import importlib
import itertools
import os
import re
from textwrap import dedent
from typing import Dict, List

from xdl.platforms import PlaceholderPlatform
from xdl.utils.schema import generate_schema

#  list of prop names that do not match pattern
PROP_NAME_EXCEPTIONS = ["pH", "LED_power", "LED_intensity", "RP_limit"]

ALL_ABSTRACT_STEPS = PlaceholderPlatform().step_library
deprecated_steps = []  # will be autopopulated on runtime

INITIAL_CATEGORIES = {
    "Liquid Handling": [
        "Add",
        "Separate",
        "Transfer",
    ],
    "Stirring": [
        "StartStir",
        "Stir",
        "StopStir",
    ],
    "Temperature Control": [
        "HeatChill",
        "HeatChillToTemp",
        "StartHeatChill",
        "StopHeatChill",
    ],
    "Inert Gas": [
        "EvacuateAndRefill",
        "Purge",
        "StartPurge",
        "StopPurge",
    ],
    "Filtration": [
        "Filter",
        "FilterThrough",
        "WashSolid",
    ],
    "Special": ["Wait", "Repeat"],
    "Other": [],
}


# File Paths
HERE = os.path.abspath(os.path.dirname(__file__))

STEP_MODULES = ["xdl.steps.templates", "xdl.steps.special"]

STEPS_OVERVIEW_RST_PATH = os.path.join(HERE, "standard", "steps_overview.rst")
FULL_STEPS_SPECIFICATION_RST_PATH = os.path.join(
    HERE, "standard", "full_steps_specification.rst"
)
STATIC_FOLDER = os.path.join(HERE, "_static")
SCHEMA_XSD_PATH = os.path.join(STATIC_FOLDER, "xdl_schema.xsd")
XDL_FILE_STRUCTURE_RST_PATH = os.path.join(HERE, "standard", "xdl_file_structure.rst")


def get_title(text, underline):
    """Return RST header with given text and underline."""
    return f"{text}\n{underline * len(text)}\n\n"


def update_categories(categories, all_steps) -> Dict[str, List[str]]:
    updated_categories = categories.copy()

    categorized_steps = list(itertools.chain(*categories.values()))
    other_steps = [step for step in all_steps if step not in categorized_steps]

    updated_categories["Other"].extend(other_steps)

    return updated_categories


CATEGORIES = update_categories(INITIAL_CATEGORIES, ALL_ABSTRACT_STEPS.keys())


def generate_steps_overview_rst() -> str:
    """Generate RST for steps overview page of XDL standard.

    Saves to RST file in docs source. Should be called before build in
    Sphinx Makefile.
    """
    rst = ""

    # Add title
    rst += get_title("Steps Overview", "=")

    # Add description
    rst += (
        "Here is an overview of all the steps implemented in this version of"
        " the XDL standard.\n\n"
    )

    # Add table
    table = (
        ".. csv-table:: Implemented Steps\n"
        "   :header: " + ",".join([f'"{item}"' for item in CATEGORIES]) + "\n\n"
    )
    table_length = max(len(steps) for steps in CATEGORIES.values())
    for idx in range(table_length):
        table += "   "
        for category_steps in CATEGORIES.values():
            try:
                table += f'"{category_steps[idx]}",'
            except IndexError:
                table += '"",'
        table = table[:-1] + "\n"
    rst += table

    # Save RST
    with open(STEPS_OVERVIEW_RST_PATH, "w") as fd:
        fd.write(rst)

    return rst


def generate_full_steps_specification_rst(steps) -> str:
    """Generate RST for full steps specification page of XDL standard.

    Saves to RST file in docs source. Should be called before build in
    Sphinx Makefile.
    """
    rst = ""

    # Add title
    rst += get_title("Full Steps Specification", "=")

    # Add steps
    for category_name, category_steps in CATEGORIES.items():

        # Add category
        rst += get_title(category_name, "*")
        for step_name in category_steps:
            if step_name in deprecated_steps:
                print(
                    f"Warning: '{step_name}' from category '{category_name}' is"
                    f" deprecated and therefore omitted from the docs."
                )
                continue
            rst += generate_step_specification_rst(steps[step_name])
            rst += "\n\n"

        rst += "\n\n"

    # Save RST
    with open(FULL_STEPS_SPECIFICATION_RST_PATH, "w") as fd:
        fd.write(rst)

    return rst


def generate_step_specification_rst(step) -> str:
    """Generate step specification RST for step from ``parse_templates`` dict."""
    rst = ""
    rst += get_title(step["name"], "^")
    rst += f'{step["description"]}\n\n'
    rst += generate_props_table_rst(step["properties"])
    return rst


def generate_props_table_rst(props_table) -> str:
    """Generate props table for step specification. ``props_table`` must be from
    step from ``parse_templates``.
    """
    rst = ""
    rst += ".. csv-table::\n"
    rst += "   :quote: $\n"
    rst += '   :header: "Property", "Type", "Description"\n\n'
    for prop in props_table:
        prop_description = prop["description"].replace('"', '\\"')
        rst += f'   $``{prop["name"]}``$, $``{prop["type"]}``$, ${prop_description}$\n'
    return rst


def generate_xdl_file_structure_rst(steps) -> str:
    """Generate RST for xdl file structure page of XDL standard.

    Saves to RST file in docs source. Should be called before build in
    Sphinx Makefile.
    """
    rst = (
        dedent(
            """\
            ==================
            XDL File Structure
            ==================

            XDL files will follow XML syntax and consist of three mandatory sections: ``Hardware``, where virtual vessels that the reaction mixture can reside in are declared. ``Reagents``, where all reagents that are used in the procedure are declared, and ``Procedure``, where the synthetic actions involved in the procedure are linearly declared. An optional, but recommended Metadata section is also available for adding in extra information about the procedure. All sections are wrapped in an enclosing ``Synthesis`` tag.

            XDL File Stub
            *************

            .. code-block:: xml

                <Synthesis>
                    <Metadata>
                        <!-- ... -->
                    </Metadata>

                    <Hardware>
                        <!-- ... -->
                    </Hardware>

                    <Reagents>
                        <!-- ... -->
                    </Reagents>

                    <Parameters>
                        <!-- ... -->
                    </Parameters>

                    <Procedure>
                        <!-- ... -->
                    </Procedure>
                </Synthesis>

            Enhanced XDL 1+ File Stub
            *************************

            XDL 1 also has an enhanced XDL XML syntax for providing additional context to syntheses. As of version 1.0.0, this is used to provide XMLBlueprint templates for executing procedures in the ``Synthesis`` section (see :ref:`bp_eg`).For full use of XMLBlueprints, the root
            node ``XDL`` must enclose the ``Synthesis`` node.

            It is recommended to use the ``XDL`` root node (as below) for all XDL files going forward, including those which do not contain blueprints.
            However, non-blueprint containing XDL files (``Synthesis`` section only) with no ``XDL`` root node (as above), will also still be compatible.

            .. code-block:: xml

                <XDL>
                    <Synthesis>
                        <Metadata>
                            <!-- ... -->
                        </Metadata>

                        <Hardware>
                            <!-- ... -->
                        </Hardware>

                        <Parameters>
                            <!-- ... -->
                        </Parameters>

                        <Reagents>
                            <!-- ... -->
                        </Reagents>

                        <Procedure>
                            <!-- ... -->
                        </Procedure>
                    </Synthesis>
                </XDL>

            Metadata
            ********

            The optional ``Metadata`` section should contain extra information about the procedure.

            """
        )
        + generate_step_specification_rst(steps["Metadata"])
        + dedent(
            """\

            .. _paramclass:

            Parameters
            **********

            The optional ``Parameters`` section can be used to define useful values (e.g. volumes, time or temperatures) that may be used multiple times in a given synthesis.
            For details on how to use parameters, see :doc:`/standard/parameters`

            Parameter
            ^^^^^^^^^

            .. csv-table::
               :quote: $
               :header: "Property", "Type", "Description"

               $``id``$, $``str``$, Brief description of the synthesis.$
               $``parameter_type``$, $``str``$, Type of the parameter i.e. 'volume', 'temp', 'time'.$
               $``value``$, $``str``$, $Optional. Value for parameter. If no other value is specified when this parameter is used, it will be used as a default value.$
               $``min``$, $``str``$, $Optional. Minimum value for parameter.$
               $``max``$, $``str``$, $Optional. Maximum value for parameter.$

            Reagents
            ********

            The ``Reagents`` section contains ``Reagent`` elements with the props below.

            """
        )
        + generate_step_specification_rst(steps["Reagent"])
        + dedent(
            """\

            Procedure
            *********
            All steps included in the :doc:`/standard/full_steps_specification` may be given within the
            ``Procedure`` block of a XDL file. Additionally, the ``Procedure`` block may be, but does not have to be, divided up into ``Prep``, ``Reaction``, ``Workup`` and ``Purification`` blocks, each of which can contain any of the steps in the specification.

            Example XDL snippet using optional Procedure subsections
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            .. code-block:: xml

                <Procedure>

                    <Prep>
                        <!-- Preparation steps here, reagent additions etc. -->
                    </Prep>

                    <Reaction>
                        <!-- Reaction steps here, heating and stirring etc. -->
                    </Reaction>

                    <Workup>
                        <!-- Workup steps here, separation, evaporation etc. -->
                    </Workup>

                    <Purification>
                        <!-- Purification steps here, column, distillation etc. -->
                    </Purification>

                </Procedure>
            """
        )
    )

    with open(XDL_FILE_STRUCTURE_RST_PATH, "w") as fd:
        fd.write(rst)

    return rst


def parse_templates():
    """Parse ``xdl.steps.templates`` and ``xdl.steps.special`` to extract
    information of all steps, ``Reagent`` and ``Metadata``.

    Returns:
        Dict[str, Dict[str, str]]: Returns dict of step names and step details
        {
            step_name: {
                "name": step_name,
                "description": step_description,
                "properties": [
                    {
                        "name": prop_name,
                        "type": prop_type,
                        "description": prop_description,
                    },
                    ...
                ]
            },
            ...
        }
    """
    global deprecated_steps

    steps = {}

    IGNORED_STEPS = ["AbstractMonitorStep"]  # noqa: N806

    CLASS_NAME_PATTERN = re.compile(  # noqa: N806
        r"^(?P<name>(?<=Abstract).+?(?=Step)|" + "|".join(CATEGORIES["Special"]) + r")$"
    )

    # Allow 'str', 'int', 'Union[List, str]' etc
    MANDATORY_PROPS_PATTERN = re.compile(  # noqa: N806
        r"^(?P<name>[a-z_]+)"
        r" \((?P<type>[A-Za-z ,\[\]]+)\):"
        r" ?(?P<description>.*)$"
    )

    for step_module in STEP_MODULES:
        module = importlib.import_module(step_module)

        names = dir(module)
        for name in names:
            if name in IGNORED_STEPS:
                continue

            extracted_name = ""
            result = CLASS_NAME_PATTERN.match(name)
            if result is not None:
                extracted_name = result.groupdict()["name"]

            is_abstract_step = name.startswith("Abstract")
            is_special_step = extracted_name in CATEGORIES["Special"]

            if not (is_abstract_step or is_special_step):
                continue

            cls = getattr(module, name)

            if cls.__xdl_deprecated__:
                deprecated_steps.append(name)
                continue

            docstring = str(cls.__doc__)

            # Infer Step name
            if is_abstract_step and not is_special_step:
                step_name = cls.MANDATORY_NAME
            else:
                step_name = name

            # Infer Step description by parsing docstring
            is_description = True
            is_mandatory_props = False
            is_new_prop_line = False
            step_description = ""
            step_properties = []
            step_property = {}
            for line in docstring.splitlines():
                line = line.strip()

                if line.startswith("Name: ") or line.lower() in [
                    "Args:".lower(),
                    "Mandatory Props:".lower(),
                ]:
                    # The first occurrence of any keyword marks the end of the
                    # description and the beginning of the mandatory_props
                    if is_description:
                        is_description = False
                        step_description = step_description.strip()

                    is_mandatory_props = True
                    continue

                if is_description:
                    step_description += line + "\n"

                if is_mandatory_props:
                    if not line:
                        continue
                    result = MANDATORY_PROPS_PATTERN.match(line)
                    is_new_prop_line = result is not None
                    if result is not None:
                        # Cursor just hit a line that starts declaration of prop
                        step_property = result.groupdict()
                        if (
                            not is_special_step
                            and step_property["name"] in cls.MANDATORY_DEFAULT_PROPS
                        ):
                            step_property["description"] = (
                                "Optional. " + step_property["description"]
                            )

                        step_properties.append(step_property)
                    if not is_new_prop_line:
                        step_property["description"] += " " + line

            steps[step_name] = {
                "name": step_name,
                "description": step_description,
                "properties": step_properties,
            }
    return steps


def generate_schema_xsd():
    """Write schema to XSD file for docs."""
    schema = generate_schema(ALL_ABSTRACT_STEPS)
    # Need to make static folder as empty folder is not committed to Git, so CI
    # fails.
    os.makedirs(STATIC_FOLDER, exist_ok=True)
    with open(SCHEMA_XSD_PATH, "w") as fd:
        fd.write(schema)


if __name__ == "__main__":
    print("Generating XDL Standard RST files...")
    steps = parse_templates()
    generate_xdl_file_structure_rst(steps)
    generate_steps_overview_rst()
    generate_full_steps_specification_rst(steps)
    generate_schema_xsd()
