import os
import pytest
from xdl import XDL
from chemputerxdl.steps import (
    Transfer, Add, Stir, Wait, Separate, SeparatePhases)
from ...utils import test_step
from xdl.errors import XDLError
from xdl.utils.sanitisation import convert_val_to_std_units

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

correct_step_info = [
    # Product bottom, single wash
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'rotavap',
            'lower_phase_port': 'evaporate',
            'upper_phase_vessel': 'waste_separator'
        }),
    ],
    # Product top, single wash
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'waste_separator',
            'upper_phase_vessel': 'rotavap',
            'upper_phase_port': 'evaporate',
        }),
    ],
    # Product bottom, single extraction
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'rotavap',
            'lower_phase_port': 'evaporate',
            'upper_phase_vessel': 'waste_separator'
        }),
    ],
    # Product top, single extraction
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'waste_separator',
            'upper_phase_vessel': 'rotavap',
            'upper_phase_port': 'evaporate',
        }),
    ],
    # Product bottom, 2 washes
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'waste_separator',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
        (Add, {}),
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'rotavap',
            'lower_phase_port': 'evaporate',
            'upper_phase_vessel': 'waste_separator'
        }),
    ],
    # Product top, 2 washes
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'waste_separator',
            'upper_phase_vessel': 'separator',
        }),
        (Add, {}),
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'upper_phase_vessel': 'rotavap',
            'upper_phase_port': 'evaporate',
            'lower_phase_vessel': 'waste_separator'
        }),
    ],
    # Product bottom, 2 extractions
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'rotavap',
            'lower_phase_port': 'evaporate',
            'upper_phase_vessel': 'separator',
        }),
        (Add, {}),
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'upper_phase_vessel': 'waste_separator',
            'lower_phase_port': 'evaporate',
            'lower_phase_vessel': 'rotavap'
        }),
    ],
    # Product top 2, extractions
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'rotavap',
            'upper_phase_port': 'evaporate',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
        (Add, {}),
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'upper_phase_vessel': 'rotavap',
            'upper_phase_port': 'evaporate',
            'lower_phase_vessel': 'waste_separator'
        }),
    ],

    # Product bottom 1 wash, to_vessel == separation_vessel
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'waste_separator',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
    ],

    # Product bottom 1 extraction, to_vessel == separation_vessel
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'waste_separator',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
    ],

    # Product top 1 wash, to_vessel == separation_vessel
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'waste_separator',
            'upper_phase_vessel': 'separator',
        }),
    ],

    # Product top 1 extraction, to_vessel == separation_vessel
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'waste_separator',
            'upper_phase_vessel': 'separator',
        }),
    ],

    # Product top 2 wash, to_vessel == separation_vessel
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'waste_separator',
            'upper_phase_vessel': 'separator',
        }),
        (Add, {}),
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'upper_phase_vessel': 'separator',
            'lower_phase_vessel': 'waste_separator'
        }),
    ],

    # Product bottom 2 wash, to_vessel == separation_vessel
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'waste_separator',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
        (Add, {}),
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'waste_separator',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
    ],

    # Product top 2 extractions, to_vessel == separation_vessel
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'buffer_flask2',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
        (Add, {}),
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'waste_separator',
            'upper_phase_vessel': 'separator',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask2',
            'to_vessel': 'separator',
        }),
    ],

    # Product bottom 2 extractions, to_vessel == separation_vessel
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'separator',
        }),
        (Add, {}),
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'waste_separator',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
    ],

    # Product top, 1 extraction, waste phase to separator, product phase to
    # rotavap
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'rotavap',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
    ],

    # Product top, 2 extractions, waste_phase_to_separator, product phase to
    # rotavap
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'rotavap',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
        (Add, {}),  # Solvent
        (Stir, {
            'stir_speed': convert_val_to_std_units(
                Separate.DEFAULT_PROPS['mixing_stir_speed']),
            'time': convert_val_to_std_units(
                Separate.DEFAULT_PROPS['mixing_time'])
        }),
        (Stir, {}),
        (Wait, {
            'time': convert_val_to_std_units(
                Separate.DEFAULT_PROPS['settling_time'])
        }),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'rotavap',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
    ],

    # Product top, 2 washes, waste_phase_to_separator, product phase to
    # rotavap
    [
        (Transfer, {}),  # Reaction mixture
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'separator',
        }),
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'rotavap',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
    ],

    # Product top, 2 washes, waste_phase_to_waste, product phase to
    # rotavap
    [
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'waste_separator',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'rotavap',
            'upper_phase_vessel': 'waste_separator',
            'lower_phase_through': 'celite',
        }),
    ],

    # Product bottom, 2 washes, waste phase to separator,
    # product phase to rotavap
    [
        (Transfer, {
            'from_vessel': 'filter',
            'to_vessel': 'separator',
        }),
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'buffer_flask',
            'upper_phase_vessel': 'buffer_flask2',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask',
            'to_vessel': 'separator',
        }),
        (Add, {}),  # Solvent
        (Stir, {}),
        (Stir, {}),
        (Wait, {}),
        (SeparatePhases, {
            'lower_phase_vessel': 'rotavap',
            'upper_phase_vessel': 'buffer_flask2',
        }),
        (Transfer, {
            'from_vessel': 'buffer_flask2',
            'to_vessel': 'separator',
        })
    ]
]

@pytest.mark.unit
def test_separate():
    """Test separating then moving through a cartridge to the final vessel."""
    xdl_f = os.path.join(FOLDER, 'separate.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    # generic_chempiler_test(xdl_f, graph_f)
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)
    assert (
        len([step for step in x.steps if step.name == 'Separate'])
        == len(correct_step_info)
    )
    i = 0
    for step in x.steps:
        if type(step) == Separate:
            current_step_info = correct_step_info[i]
            try:
                assert len(current_step_info) == len(step.steps)
            except AssertionError:
                raise AssertionError(
                    f'Step: {i} ({len(current_step_info)} {len(step.steps)})\n\
 {step.properties}\n\n{current_step_info}')
            for j, substep in enumerate(step.steps):
                try:
                    test_step(substep, current_step_info[j])
                except AssertionError:
                    raise AssertionError(
                        f'Step: {i} {step.properties}\n\n{substep.properties}')
            i += 1
    assert i == len(correct_step_info)

@pytest.mark.unit
def test_separate_without_enough_buffer_flasks():
    with pytest.raises(XDLError):
        xdl_f = os.path.join(FOLDER, 'separate_no_buffers.xdl')
        graph_f = os.path.join(FOLDER, 'separate_no_buffers.json')
        x = XDL(xdl_f)
        x.prepare_for_execution(graph_f, testing=True)

@pytest.mark.unit
def test_separate_more_than_max_volume():
    xdl_f = os.path.join(FOLDER, 'separate_more_than_max_volume.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)
    for step in x.steps:
        if step.name == 'Separate':
            assert step.n_separations == 2
            assert step.solvent_volume == 75
