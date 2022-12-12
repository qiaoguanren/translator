import pytest
import os
from xdl import XDL
from chemputerxdl.steps import Shutdown

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')
INTEGRATION_FOLDER = os.path.join(os.path.dirname(HERE), 'integration', 'files')

@pytest.mark.unit
def test_xdl_ends_with_shutdown():
    x = XDL(os.path.join(FOLDER, "dissolve_in_rotavap.xdl"))
    graph_f = os.path.join(FOLDER, "bigrig.json")
    x.prepare_for_execution(graph_f, testing=True)
    assert type(x.steps[-1]) == Shutdown
    shutdown = x.steps[-1]

    assert len(shutdown.steps) == 17

    chiller_shutdown = False
    flask_chiller_shutdown = False

    stirrer_separator_shutdown = False
    stirrer_filter_shutdown = False
    stirrer_flask_shutdown = False
    stirrer_reactor_shutdown = False

    vacuum_rotavap_stopped = False
    vacuum_rotavap_vented = False
    vacuum_filter_stopped = False
    vacuum_filter_vented = False
    vacuum_reactor_stopped = False
    vacuum_reactor_vented = False

    rotavap_up = False
    rotavap_stopped_rotation = False
    rotavap_stopped_heating = False

    heater_reactor_shutdown = False

    for step in shutdown.steps:
        if step.name == 'CStopChiller':
            if step.vessel == 'filter':
                chiller_shutdown = True

            elif step.vessel == 'flask_water':
                flask_chiller_shutdown = True

        elif step.name == 'CStopVacuum':
            if step.vessel == 'vacuum_flask':
                vacuum_filter_stopped = True

            elif step.vessel == 'rotavap':
                vacuum_rotavap_stopped = True

            elif step.vessel == 'vacuum_reactor_flask':
                vacuum_reactor_stopped = True

        elif step.name == 'CVentVacuum':
            if step.vessel == 'vacuum_flask':
                vacuum_filter_vented = True

            elif step.vessel == 'rotavap':
                vacuum_rotavap_vented = True

            elif step.vessel == 'vacuum_reactor_flask':
                vacuum_reactor_vented = True

        elif step.name == 'CStopStir':
            if step.vessel == 'filter':
                stirrer_filter_shutdown = True

            elif step.vessel == 'separator':
                stirrer_separator_shutdown = True

            elif step.vessel == 'reactor':
                stirrer_reactor_shutdown = True

            elif step.vessel == 'flask_water':
                stirrer_flask_shutdown = True

        elif step.name == 'CRotavapStopRotation':
            if step.rotavap_name == 'rotavap':
                rotavap_stopped_rotation = True

        elif step.name == 'CRotavapStopHeater':
            if step.rotavap_name == 'rotavap':
                rotavap_stopped_heating = True

        elif step.name == 'CRotavapLiftUp':
            if step.rotavap_name == 'rotavap':
                rotavap_up = True

        elif step.name == 'CStopHeat':
            if step.vessel == 'reactor':
                heater_reactor_shutdown = True

    assert chiller_shutdown
    assert flask_chiller_shutdown

    assert stirrer_separator_shutdown
    assert stirrer_filter_shutdown
    assert stirrer_flask_shutdown
    assert stirrer_reactor_shutdown

    assert vacuum_rotavap_stopped
    assert vacuum_rotavap_vented
    assert vacuum_filter_stopped
    assert vacuum_filter_vented
    assert vacuum_reactor_stopped
    assert vacuum_reactor_vented

    assert rotavap_up
    assert rotavap_stopped_rotation
    assert rotavap_stopped_heating

    assert heater_reactor_shutdown
