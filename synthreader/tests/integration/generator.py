from typing import List, Dict
from synthreader.tagging import tag_synthesis
from synthreader.interpreting import extract_actions
from synthreader.finishing import action_list_to_xdl
from synthreader.words import (
    ReagentGroupWord, ReagentWord, SolutionWord, AbstractReagentWord, Word)
from synthreader.words.modifiers import ReagentModifier, MethodModifier
from chemputerxdl.steps import Transfer
import os

HERE = os.path.abspath(os.path.dirname(__file__))
ALL_TESTS_FILE = os.path.join(HERE, 'all_tests.py')

VESSEL_KEYWORDS = [
    'through',
    'from_vessel',
    'filter_vessel',
    'waste_phase_to_vessel',
    'vessel',
    'to_vessel',
    'separation_vessel',
    'through_cartridge',
    'rotavap_name',
    'column'
]

def generate_test_info(text, name, save_file):
    x = tag_synthesis(text)
    reagents = get_reagents(x)
    x = extract_actions(x)
    x = action_list_to_xdl(x)
    steps = get_step_types(x)
    vessels = get_vessels(x)
    properties = get_properties(x)
    write_to_file(text, x, reagents, steps, vessels, properties, name, save_file)
    generate_test_info_init_file()
    generate_all_tests_file()

def get_vessels(x):
    vessels = []
    for step in x.steps:
        step_vessels = {}
        for prop, val in step.properties.items():
            if prop in VESSEL_KEYWORDS and val:
                step_vessels[prop] = val
        vessels.append(step_vessels)
    return vessels

def get_properties(x):
    props = []
    for step in x.steps:
        step_props = {}
        defaults, internals = [], []
        defaults = step.DEFAULT_PROPS
        internals = step.INTERNAL_PROPS
        for prop, val in step.properties.items():
            if prop not in VESSEL_KEYWORDS and val != None:
                if not (prop in defaults and defaults[prop] == val):
                    if not prop in internals:
                        step_props[prop] = val
        props.append(step_props)
    return props

def write_to_file(syntext, xdl_obj, reagents, steps, vessels, properties, name, save_file):
    upper_name = name.upper()
    indent = ' ' * 4
    s = 'from xdl.steps import *\n\n'

    # Text
    s += f"{upper_name}_TEXT = '''{syntext}'''\n\n"
    s += f"{upper_name}_INFO = {{\n{indent}'text': {upper_name}_TEXT,\n"
    s += f"{indent}'name': '{name.lower()}',\n"

    # Reagents
    s += f"{indent}'reagents': {{\n"
    for reagent in reagents:
        if "'" in reagent:
            s += f'{indent * 2}"{reagent}": {{\n'
        else:
            s += f"{indent * 2}'{reagent}': {{\n"
        s += f"{indent * 3}'quantities': ["
        for quantity in reagents[reagent]['quantities']:
            s += f"'{str(quantity)}', "
        if reagents[reagent]['quantities']:
            s = s[:-2]
        s += f"],\n{indent * 2}}},\n"
    s += f"{indent}}},\n"

    # Steps
    s += f"{indent}'steps': [\n"
    for step in steps:
        s += f"{indent * 2}{step},\n"
    s += f"{indent}],\n"

    # Vessels
    s += f"{indent}'vessels': [\n"
    for i, step_vessels in enumerate(vessels):
        s += f"{indent*2}# {xdl_obj.steps[i].name}\n"
        if not step_vessels:
            s += f"{indent*2}{{}},\n"
        else:
            s += f"{indent*2}{{\n"
            for prop, val in step_vessels.items():
                val = val
                s += f"{indent*3}'{prop}': '{val}',\n"
            s += f"{indent*2}}},\n"
    s += f"{indent}],\n"


    # Properties
    s += f"{indent}'properties': [\n"
    for i, step_props in enumerate(properties):
        s += f"{indent*2}# {xdl_obj.steps[i].name}\n"
        if not step_props:
            s += f"{indent*2}{{}},\n"
        else:
            s += f"{indent*2}{{\n"
            for prop, val in step_props.items():
                if prop == 'children':
                    continue
                if type(val) == str:
                    if "'" in val:
                        val = f'"{val}"'
                    else:
                        val = f"'{val}'"
                s += f"{indent*3}'{prop}': {val},\n"
            s += f"{indent*2}}},\n"
    s += f"{indent}],\n"

    s += "}\n"
    with open(save_file, 'w') as fileobj:
        fileobj.write(s)

def get_step_types(xdl_obj):
    steps = []
    for step in xdl_obj.steps:
        if type(step) != Transfer:
            steps.append(step.name)
    return steps

def get_reagents(tagged_synthesis: List[List[Word]]) -> Dict:
    """Get dict of reagents as found in test infos from tagged synthesis.

    Args:
        tagged_synthesis (List[List[Word]]): Return from
            synthreader.tag_synthesis

    Returns:
        Dict: Dict like those found in test info files of reagents in synthesis.
    """
    reagents = {}
    for sentence in tagged_synthesis:
        for word in sentence:
            update_reagent_dict(word, reagents)
    return reagents

def update_reagent_dict(word: Word, reagent_dict: Dict) -> None:
    """Recursive function. Finds ReagentWord objects in all sorts of other
    objects recursively, and adds them to reagent_dict.

    Args:
        word (Word): Word to recursively search for ReagentWords.
        reagent_dict (Dict): Dict to add reagents found in word to.
    """
    if type(word) == ReagentModifier:
        for reagent in word.reagents:
            update_reagent_dict(reagent, reagent_dict)

    elif type(word) == MethodModifier:
        for word in word.words:
            if isinstance(word, AbstractReagentWord):
                update_reagent_dict(word, reagent_dict)

    elif type(word) == ReagentGroupWord:
        for sub_reagent in word.reagents:
            update_reagent_dict(sub_reagent, reagent_dict)

    elif type(word) == SolutionWord:
        for solute in word.solutes:
            update_reagent_dict(solute, reagent_dict)
        update_reagent_dict(word.solvent, reagent_dict)

    # Exit from recursive calls. If ReagentWord reached add it to reagent_dict
    elif type(word) == ReagentWord:
        quantities = [str(quantity) for quantity in word.quantities]
        if word.name in reagent_dict:
            reagent_dict[word.name]['quantities'].extend(quantities)
        else:
            reagent_dict[word.name] = {'quantities': quantities}

def generate_test_info_init_file():
    s = ''
    for f in sorted(os.listdir(os.path.join(HERE, 'test_info'))):
        if not f.startswith('_'):
            name = os.path.splitext(f)[0]
            s += f'from .{name} import {name.upper()}_INFO\n'
    with open(os.path.join(HERE, 'test_info', '__init__.py'), 'w') as fd:
        fd.write(s)

def generate_all_tests_file():
    s = '''
from .test_reagents import test_reagents
from .test_step_types import test_correct_step_types
from  .test_properties import test_correct_vessels, test_correct_properties
from .test_info import *
from synthreader.tagging import tag_synthesis
from synthreader.interpreting import extract_actions
from synthreader.finishing import action_list_to_xdl
import pytest
'''
    from . import test_info
    import inspect
    for synthesis_info in sorted([
        item
        for item in inspect.getmembers(test_info)
        if item[0].upper() == item[0]
    ], key=lambda x: x[0]):
        name = synthesis_info[1]['name']
        upper_name = name.upper()
        s += f'''
# {upper_name}
@pytest.mark.integration
def test_{name}_reagents():
    test_reagents({upper_name}_INFO)

@pytest.mark.integration
def test_{name}_step_types():
    test_correct_step_types({upper_name}_INFO)

@pytest.mark.integration
def test_{name}_vessels():
    test_correct_vessels({upper_name}_INFO)
'''
        if 'properties' in synthesis_info[1]:
            s += f'''
@pytest.mark.integration
def test_{name}_properties():
    test_correct_properties({upper_name}_INFO)

@pytest.mark.fast_integration
def test_{name}():
    tagged_synthesis = tag_synthesis({upper_name}_INFO["text"])
    test_reagents({upper_name}_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types({upper_name}_INFO, x)
    test_correct_vessels({upper_name}_INFO, x)
    test_correct_properties({upper_name}_INFO, x)
'''
    with open(ALL_TESTS_FILE, 'w') as fd:
        fd.write(s)
