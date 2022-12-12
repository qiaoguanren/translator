import pytest
from chemputerxdl.steps import Add, Dry

EQUIVALENT_VOLUMES = (500, [
    '500 mL',
    '500ml',
    '0.5l',
    '500',
    '500000 ul',
    '50 cl',
    '5 dl',
])

EQUIVALENT_MASSES = (1, [
    '1 g',
    '0.001kg',
    '1',
    '1000 mg',
    '1000000  ug',
])

EQUIVALENT_PRESSURES = (1013.25, [
    '1013.25 mbar',
    '1.01325bar',
    '101325 Pa',
    '1 atm',
    '760Torr',
    '760 mmhg',
    '1013.25',
])

EQUIVALENT_TEMPERATURES = (25, [
    '25',
    '25°C',
    '77 F',
    '298.15K',
])

EQUIVALENT_TIMES = (3600, [
    '3600',
    '3600s',
    '3600 secs',
    '3600 sec',
    '3600 seconds',
    '60 min',
    '60m',
    '60 mins',
    '60minutes',
    '1h',
    '1 hr',
    '1 hrs',
    '1 hours',
    '1 hour',
])

@pytest.mark.unit
def test_volume_conversion():
    correct_volume = EQUIVALENT_VOLUMES[0]
    for volume in EQUIVALENT_VOLUMES[1]:
        step = Add(
            reagent='water', volume=volume, vessel='filter')
        assert step.volume == correct_volume

@pytest.mark.unit
def test_mass_conversion():
    correct_mass = EQUIVALENT_MASSES[0]
    for mass in EQUIVALENT_MASSES[1]:
        step = Add(
            reagent='water', mass=mass, vessel='filter')
        assert step.mass == correct_mass

@pytest.mark.unit
def test_pressure_conversion():
    correct_pressure = EQUIVALENT_PRESSURES[0]
    for pressure in EQUIVALENT_PRESSURES[1]:
        step = Dry(vessel='filter', vacuum_pressure=pressure)
        assert (f'{step.vacuum_pressure:.2f}' == f'{correct_pressure:.2f}')

@pytest.mark.unit
def test_temperature_conversion():
    correct_temp = EQUIVALENT_TEMPERATURES[0]
    for temp in EQUIVALENT_TEMPERATURES[1]:
        step = Dry(vessel='filter', temp=temp)
        assert step.temp == correct_temp

@pytest.mark.unit
def test_time_conversion():
    correct_time = EQUIVALENT_TIMES[0]
    for time in EQUIVALENT_TIMES[1]:
        step = Dry(vessel='filter', time=time)
        assert step.time == correct_time
