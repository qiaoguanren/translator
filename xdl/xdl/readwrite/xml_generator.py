from typing import List
from lxml import etree
from ..reagents import Reagent
from ..hardware import Hardware
from ..steps import Step
from ..constants import XDL_VERSION
from ..utils.misc import format_property
from ..utils.sanitisation import convert_val_to_std_units
if False:
    from ..xdl import XDL

def xdl_to_xml_string(
    xdl_obj: 'XDL',
    full_properties: bool = False,
    full_tree: bool = False,
    graph_hash: str = None
) -> str:
    """Convert given XDL object to XML string.

    Args:
        xdl_obj (XDL): XDL object to convert to XML string.
        full_properties (bool): If True, all properties will be written.
            If False only mandatory, non default values and always write
            properties will be written.
        full_tree (bool): If True, full step tree will be written as is the case
            in xdlexe files.
        graph_hash (str): Hash of graph to include in xdlexe files.

    Returns:
        str: Pretty printed XML string of procedure.
    """
    xml_tree = get_xdl_tree(xdl_obj, full_properties, full_tree, graph_hash)
    return _get_xdl_string(xml_tree)

def step_to_xml_string(
    step: Step,
    full_properties: bool = False,
    full_tree: bool = False,
) -> str:
    """Get pretty printed XML string of given step.

    Args:
        step (Step): Step to get XDLEXE string for.
        full_properties (bool): If True, all properties will be written.
            If False only mandatory, non default values and always write
            properties will be written.
        full_tree (bool): If True, full step tree will be written as is the case
            in xdlexe files.
    """
    step_tree = _get_step_tree(step, full_properties, full_tree)
    return _get_element_xdl_string(step_tree)


#######################
# XML Tree Generation #
#######################

def get_xdl_tree(
    xdl_obj: 'XDL',
    full_properties: bool = False,
    full_tree: bool = False,
    graph_hash: int = None
):
    steps = xdl_obj.steps
    reagents = xdl_obj.reagents
    hardware = xdl_obj.hardware

    # Create <Synthesis> tag with graph hash if given.
    xdltree = etree.Element('Synthesis')
    if graph_hash:
        xdltree.attrib['graph_sha256'] = graph_hash

    # Add <Hardware /> section to tree
    _append_hardware_tree(xdltree, hardware)

    # Add <Reagents /> section to tree
    _append_reagents_tree(xdltree, reagents)

    # Add <Procedure  /> section to tree
    _append_procedure_tree(
        xdltree, steps, full_properties=full_properties, full_tree=full_tree)

    return xdltree

def _append_hardware_tree(
        xdltree: etree.ElementTree, hardware: Hardware) -> None:
    """Create and add Hardware section to XDL tree."""
    hardware_tree = etree.Element('Hardware')
    for component in hardware:
        component_tree = etree.Element('Component')
        for prop in component.PROP_TYPES:
            val = component.properties[prop]
            if val is not None:
                if prop == 'component_type':
                    component_tree.attrib['type'] = str(val)
                else:
                    component_tree.attrib[prop] = str(val)
        hardware_tree.append(component_tree)
    xdltree.append(hardware_tree)

def _append_reagents_tree(
        xdltree: etree.ElementTree, reagents: List[Reagent]) -> None:
    """Create and add Reagents section to XDL tree."""
    reagents_tree = etree.Element('Reagents')
    for reagent in reagents:
        reagent_tree = etree.Element('Reagent')
        for prop in reagent.PROP_TYPES:
            val = reagent.properties[prop]
            if val:
                reagent_tree.attrib[prop] = str(val)
        reagents_tree.append(reagent_tree)
    xdltree.append(reagents_tree)

def _append_procedure_tree(
    xdltree: etree.ElementTree,
    steps: List[Step],
    full_properties: bool = False,
    full_tree: bool = False,
) -> None:
    """Create and add Procedure section to XDL tree."""
    procedure_tree = etree.Element('Procedure')
    for step in steps:
        procedure_tree.append(_get_step_tree(
            step, full_properties=full_properties, full_tree=full_tree))
    xdltree.append(procedure_tree)

def _get_step_tree(
    step: Step,
    full_properties: bool = False,
    full_tree: bool = False,
):
    """Get XML tree associated with given step.

    Args:
        step (Step): Step to generate XML tree for.
        full_properties (bool): If True, all properties will be written.
            If False only mandatory, non default values and always write
            properties will be written.
        full_tree (bool): If True, full step tree will be written as is the case
            in xdlexe files.
    """
    step_tree = etree.Element(step.name)
    children = False
    for prop in step.PROP_TYPES:
        # Find out if step has children, and if they should be written (xdlexe)
        if (prop == 'children'
            and step.properties[prop]
                and full_properties):
            children = True

        # Add property to step tree
        _add_step_property(
            step_tree,
            step,
            prop,
            full_properties=full_properties,
            full_tree=full_tree
        )

    if full_tree:
        # Nested elements like Repeat have Steps and Children instead of
        # just raw steps
        if children:
            children_steps_tree = etree.Element('Steps')
            for substep in step.steps:
                children_steps_tree.append(
                    _get_step_tree(
                        substep,
                        full_properties=full_properties,
                        full_tree=full_tree
                    )
                )
            step_tree.append(children_steps_tree)
        else:
            for substep in step.steps:
                step_tree.append(
                    _get_step_tree(
                        substep,
                        full_properties=full_properties,
                        full_tree=full_tree,
                    )
                )
    return step_tree

def _add_step_property(
    step_tree: etree.Element,
    step: Step,
    prop: str,
    full_properties: bool = False,
    full_tree: bool = False,
):
    """Add given property to step tree of given step.

    Args:
        step_tree (etree.Element): Step tree to add property to.
        step (Step): Step corresponding to step_tree.
        prop (str): Property to add to step_tree.
        full_properties (bool): If True, all properties will be written.
            If False only mandatory, non default values and always write
            properties will be written.
        full_tree (bool): If True, full step tree will be written as is the case
            in xdlexe files. This applies to 'children' property.
    """
    val = step.properties[prop]
    if prop == 'children' and val:
        if full_properties:
            children_tree = etree.Element('Children')
            for child in val:
                child_tree = _get_step_tree(
                    child, full_properties=full_properties, full_tree=full_tree)
                children_tree.append(child_tree)
            step_tree.append(children_tree)
        else:
            for child in val:
                step_tree.append(_get_step_tree(
                    child, full_properties=full_properties, full_tree=full_tree
                ))
    else:
        if val is not None or full_properties:
            # if self.full_properties is False ignore some properties.
            if not full_properties:

                # Don't write properties that are the same as the
                # default.
                if (prop in step.DEFAULT_PROPS
                        and convert_val_to_std_units(
                            step.DEFAULT_PROPS[prop]) == val):

                    # Some things should always be written even if they
                    # are default.
                    if prop not in step.ALWAYS_WRITE:
                        return

                # Don't write internal properties.
                if prop in step.INTERNAL_PROPS:
                    return
            # Convert value to nice units and add to element attrib.
            formatted_property = format_property(
                prop,
                val,
                step.PROP_TYPES[prop],
                step.PROP_LIMITS.get(prop, None),
                human_readable=False
            )

            if formatted_property is None:
                formatted_property = str(formatted_property)

            step_tree.attrib[prop] = formatted_property

###############################
# String Generation from Tree #
###############################

def _get_element_xdl_string(
        element: etree._ElementTree, indent_level=0, indent='  ') -> str:
    """Return given Step, Reagent or Component XML tree as pretty printed XML
    string.

    Args:
        element (etree._ElementTree): Step, Reagent or Component XML tree to
            convert to string.
        indent_level (int): Defaults to 0. Used by this function to handle
            indendation during recursive calls.
        indent (str): Defaults to '  '. Indent to use for pretty printing XML
            string.

    Returns:
        str: Pretty printed XML string of given XML tree.
    """
    s = ''
    s += f'{indent * indent_level}<{element.tag}\n'
    has_children = list(element.findall('*'))
    indent_level += 1
    # Element Properties
    for attr, val in element.attrib.items():
        if val is not None:
            s += f'{indent * indent_level}{attr}="{val}"\n'
    if has_children:
        s = s[:-1] + '>\n'
    else:
        s = s[:-1] + ' />\n'
    for subelement in element.findall('*'):
        s += _get_element_xdl_string(
            subelement, indent_level=indent_level, indent=indent)
    indent_level -= 1
    if has_children:
        s += f'{indent * indent_level}</{element.tag}>\n'
    return s

def _get_xdl_string(xdltree: etree._ElementTree) -> str:
    """Convert XDL etree to pretty XML string.

    Args:
        xdltree (etree.ElementTree): etree of XDL

    Returns:
        str: XML string
    """
    indent = '  '
    # Synthesis tag
    s = f'<?xdl version="{XDL_VERSION}" ?>\n\n'
    s += '<Synthesis'
    if xdltree.attrib:
        s += '\n'
        for prop in xdltree.attrib:
            s += f'{indent}{prop}="{xdltree.attrib[prop]}"\n'
    s += '>\n'
    indent_level = 1
    # Hardware, Reagents and Procedure tags
    for element in xdltree.findall('*'):
        s += f'{indent * indent_level}<{element.tag}>\n'
        indent_level += 1
        # Component, Reagent and Step tags
        for element2 in element.findall('*'):
            s += _get_element_xdl_string(
                element2, indent=indent, indent_level=indent_level)
        indent_level -= 1
        s += f'{indent * indent_level}</{element.tag}>\n\n'
    s += '</Synthesis>\n'
    return s
