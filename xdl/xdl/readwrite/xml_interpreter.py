import logging
from typing import Dict, List, Any
from lxml import etree
from .validation import check_attrs_are_valid
from .utils import read_file
from ..constants import SYNTHESIS_ATTRS
from ..utils import parse_bool
from ..errors import XDLError
from ..steps import Step, AbstractBaseStep
from ..reagents import Reagent
from ..hardware import Hardware, Component

# For type annotations
if False:
    from ..execution.abstract_platform import AbstractPlatform

def xdl_file_to_objs(
    xdl_file: str,
    platform: 'AbstractPlatform',
    logger: logging.Logger,
) -> Dict[str, Any]:
    """Given XDL file return steps, hardware and reagents.

    Arguments:
        xdl_file (str): Path to XDL file.

    Returns:
        Dict: (steps, hardware, reagents)
                steps: List of Step objects.
                hardware: Hardware object.
                reagents: List of Reagent objects.
    """
    xdlstr = read_file(xdl_file)
    return xdl_str_to_objs(
        xdl_str=xdlstr, logger=logger, platform=platform
    )

def xdl_str_to_objs(
    xdl_str: str,
    platform: 'AbstractPlatform',
    logger: logging.Logger,
) -> Dict[str, Any]:
    """Given XDL str return steps, hardware and reagents.

    Arguments:
        xdl_str (str): XDL str.

    Returns:
        Tuple: (steps, hardware, reagents)
                  steps: List of Step objects.
                  hardware: Hardware object.
                  reagents: List of Reagent objects.
    """
    if xdl_str:
        steps, step_record = steps_from_xdl(xdl_str, platform)
        hardware = hardware_from_xdl(xdl_str)
        reagents = reagents_from_xdl(xdl_str)
        synthesis_attrs = synthesis_attrs_from_xdl(xdl_str)
        if 'graph_sha256' in synthesis_attrs:
            assert len(steps) == len(step_record)
            for i, step in enumerate(steps):
                apply_step_record(step, step_record[i])

        parsed_xdl = {
            'steps': steps,
            'hardware': hardware,
            'reagents': reagents,
        }
        parsed_xdl['procedure_attrs'] = synthesis_attrs
        return parsed_xdl
    else:
        raise XDLError('Empty XDL given.')
    return None

def apply_step_record(step, step_record_step):
    assert step.name == step_record_step[0]
    for prop in step.properties:
        if prop != 'children' and prop != 'uuid':
            if prop not in step_record_step[1]:
                raise XDLError(f"Property {prop} missing from\
 Step {step_record_step[0]}\nThis file was most likely generated from an\
 older version of XDL. Regenerate the XDLEXE file using the latest\
 version of XDL.")
            step.properties[prop] = step_record_step[1][prop]
    step.update()
    if not isinstance(step, AbstractBaseStep):
        try:
            assert len(step.steps) == len(step_record_step[2])
        except AssertionError:
            raise AssertionError(f'{step.steps}\n\n{step_record_step[2]}\
 {len(step.steps)} {len(step_record_step[2])}')
        for j, substep in enumerate(step.steps):
            apply_step_record(substep, step_record_step[2][j])

def synthesis_attrs_from_xdl(xdl_str: str) -> Dict[str, Any]:
    """Return attrs from <Synthesis> tag.

    Arguments:
        xdl_str (str): XDL string.

    Returns:
        dict: attr dict from <Synthesis> tag.
    """
    raw_attr = etree.fromstring(xdl_str).attrib
    processed_attr = {}
    for attr in SYNTHESIS_ATTRS:
        if attr['name'] in raw_attr:
            processed_attr[attr['name']] = raw_attr[attr['name']]
            if attr['type'] == bool:
                processed_attr[attr['name']] = parse_bool(
                    raw_attr[attr['name']])
    return processed_attr

def steps_from_xdl(xdl_str: str, platform: 'AbstractPlatform') -> List[Step]:
    """Given XDL str return list of Step objects.

    Arguments:
        xdl_str (str): XDL str.

    Returns:
        List[Step]: List of Step objects corresponding to procedure described
                      in xdl_str.
    """
    steps = []
    xdl_tree = etree.fromstring(xdl_str)
    for element in xdl_tree.findall('*'):
        if element.tag == 'Procedure':
            step_record = get_full_step_record(element)
            for step_xdl in element.findall('*'):
                steps.append(xdl_to_step(step_xdl, platform.step_library))
    return steps, step_record

def get_base_steps(step):
    base_steps = []
    children = step.findall('*')
    if children:
        for child in children:
            base_steps.extend(get_base_steps(child))
    else:
        return [step]
    return base_steps

def hardware_from_xdl(xdl_str: str) -> Hardware:
    """Given XDL str return Hardware object.

    Arguments:
        xdl_str (str): XDL str.

    Returns:
        Hardware: Hardware object containing all Component objects described
                    by XDL.
    """
    return Hardware(components_from_xdl(xdl_str))

def components_from_xdl(xdl_str: str) -> List[Component]:
    """Given XDL str return list of Component objects.

    Arguments:
        xdl_str (str): XDL str.

    Returns:
        List[Component]: List of Component objects corresponding to
                           components described in xdl_str.
    """
    components = []
    xdl_tree = etree.fromstring(xdl_str)
    for element in xdl_tree.findall('*'):
        if element.tag == 'Hardware':
            for component_xdl in element.findall('*'):
                components.append(xdl_to_component(component_xdl))
    return components

def reagents_from_xdl(xdl_str: str) -> List[Reagent]:
    """Given XDL str return list of Reagent objects.

    Arguments:
        xdl_str (str): XDL str.

    Returns:
        List[Reagent]: List of Reagent objects corresponding to reagents
                         described in xdl_str.
    """
    reagents = []
    xdl_tree = etree.fromstring(xdl_str)
    for element in xdl_tree.findall('*'):
        if element.tag == 'Reagents':
            for reagent_xdl in element.findall('*'):
                reagents.append(xdl_to_reagent(reagent_xdl))
    return reagents

def xdl_to_step(
    xdl_step_element: etree._Element,
    step_type_dict: Dict[str, type]
) -> Step:
    """Given XDL step element return corresponding Step object.

    Arguments:
       xdl_step_element (lxml.etree._Element): XDL step lxml element.

    Returns:
        Step: Step object corresponding to step in xdl_step_element.
    """
    # Check if step name is valid and get step class.
    if xdl_step_element.tag not in step_type_dict:
        raise XDLError(f'{xdl_step_element.tag} is not a valid step type.')

    child_element_tags = [e.tag for e in xdl_step_element.findall('*')]
    children_steps = []
    # Nested elements like Repeat have Steps and Children elements
    # instead of just raw steps
    if 'Steps' in child_element_tags and 'Children' in child_element_tags:
        for child_element in xdl_step_element.findall('*'):
            if child_element.tag == 'Children':
                for child_step in child_element.findall('*'):
                    children_steps.append(
                        xdl_to_step(child_step, step_type_dict))
    else:
        children = xdl_step_element.findall('*')
        for child in children:
            children_steps.append(xdl_to_step(child, step_type_dict))

    step_type = step_type_dict[xdl_step_element.tag]
    # Check all attributes are valid.
    attrs = dict(xdl_step_element.attrib)
    check_attrs_are_valid(attrs, step_type)
    for attr in attrs:
        if attrs[attr].lower() == 'none':
            attrs[attr] = None

    if (not issubclass(step_type, AbstractBaseStep)
            and 'children' in step_type.__init__.__annotations__):
        attrs['children'] = children_steps

    # Try to instantiate step, any invalid values given will throw an error
    # here.
    step = step_type(**attrs)
    return step

def xdl_to_component(xdl_component_element: etree._Element) -> Component:
    """Given XDL component element return corresponding Component object.

    Arguments:
       xdl_component_element (lxml.etree._Element): XDL component lxml
                                                      element.

    Returns:
        Component: Component object corresponding to component in
                     xdl_component_element.
    """
    attrs = dict(xdl_component_element.attrib)
    # Check 'id' is in attrs..
    if 'id' not in attrs:
        raise XDLError(
            "'id' attribute not specified for component.")
    #  Check 'type' is in attrs.
    if 'type' not in attrs:
        raise XDLError(
            f"'type' attribute not specified for {attrs['id']} component.")
    check_attrs_are_valid(attrs, Component)
    # Rename 'type' attr to 'component_type' to avoid conflict with Python
    # built-in function type.
    attrs['component_type'] = attrs['type']
    del attrs['type']
    # Try to instantiate components, any invalid values given will throw an
    # error here.
    component = Component(**attrs)
    return component

def xdl_to_reagent(xdl_reagent_element: etree._Element) -> Reagent:
    """Given XDL reagent element return corresponding Reagent object.

    Arguments:
        xdl_reagent_element (lxml.etree._Element): XDL reagent lxml element.

    Returns:
        Reagent: Reagent object corresponding to reagent in
                   xdl_reagent_element.
    """
    # Check attrs are valid for Reagent
    attrs = dict(xdl_reagent_element.attrib)
    if 'id' not in attrs:
        raise XDLError(
            "'id' attribute not specified for reagent.")
    check_attrs_are_valid(attrs, Reagent)
    # Try to instantiate Reagent object and return it.
    reagent = Reagent(**attrs)
    return reagent


##########################
# .xdlexe interpretation #
##########################

def get_full_step_record(procedure_tree):
    step_record = []
    for step in procedure_tree.findall('*'):
        step_record.append(get_single_step_record(step))
    return step_record

def get_single_step_record(step_element):
    children = []
    child_element_tags = [
        element.tag for element in step_element.findall('*')]
    # Nested elements like Repeat have Steps and Children elements
    # instead of just raw steps
    if 'Steps' in child_element_tags and 'Children' in child_element_tags:
        for child_element in step_element.findall('*'):
            if child_element.tag == 'Steps':
                for step in child_element.findall('*'):
                    children.append(get_single_step_record(step))
                break
    else:
        for step in step_element.findall('*'):
            children.append(get_single_step_record(step))
    return (step_element.tag, step_element.attrib, children)
