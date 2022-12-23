import pytest

try:
    from chemputerxdl.steps import Add, AddSolid, Dry
except ModuleNotFoundError:
    pass

from xdl.reagents import Reagent

EQUIVALENT_VOLUMES = (
    500,
    [
        "500 mL",
        "500ml",
        "0.5l",
        "500",
        "500000 ul",
        "50 cl",
        "5 dl",
    ],
)

EQUIVALENT_MASSES = (
    1,
    [
        "1 g",
        "0.001kg",
        "1",
        "1000 mg",
        "1000000  ug",
    ],
)

EQUIVALENT_PRESSURES = (
    1013.25,
    [
        "1013.25 mbar",
        "1.01325bar",
        "101325 Pa",
        "1 atm",
        "760Torr",
        "760 mmhg",
        "1013.25",
    ],
)

EQUIVALENT_TEMPERATURES = (
    25,
    [
        "25",
        "25°C",
        "77 F",
        "298.15K",
    ],
)

EQUIVALENT_TIMES = (
    3600,
    [
        "3600",
        "3600s",
        "3600 secs",
        "3600 sec",
        "3600 seconds",
        "60 min",
        "60m",
        "60 mins",
        "60minutes",
        "1h",
        "1 hr",
        "1 hrs",
        "1 hours",
        "1 hour",
    ],
)

EQUIVALENT_MOLECULAR_WEIGHTS = (
    40,
    ["40 g/mol", "40g/mol", "40000 mg/mol", "40000000 ug/mol"],
)

EQUIVALENT_DENSITIES = (
    20.5,
    [
        "20.5 g/mL",
        "20.5g/ml",
        "20.5 g/cm3",
        "20500 mg/mL",
        "20500 mg/cm3",
        "20500000 ug/cm3",
        "20500000 ug/mL",
    ],
)

EQUIVALENT_CONCENTRATIONS = (
    1.5,
    [
        "1.5 mol/L",
        "1.5mol/l",
        "1500 mmol/L",
    ],
)


@pytest.mark.chemputer
def test_volume_conversion():
    correct_volume = EQUIVALENT_VOLUMES[0]
    for volume in EQUIVALENT_VOLUMES[1]:
        step = Add(reagent="water", volume=volume, vessel="filter")
        assert step.volume == correct_volume


@pytest.mark.chemputer
def test_mass_conversion():
    correct_mass = EQUIVALENT_MASSES[0]
    for mass in EQUIVALENT_MASSES[1]:
        step = AddSolid(reagent="water", mass=mass, vessel="filter")
        assert step.mass == correct_mass


@pytest.mark.chemputer
def test_pressure_conversion():
    correct_pressure = EQUIVALENT_PRESSURES[0]
    for pressure in EQUIVALENT_PRESSURES[1]:
        step = Dry(vessel="filter", pressure=pressure)
        assert f"{step.pressure:.2f}" == f"{correct_pressure:.2f}"


@pytest.mark.chemputer
def test_temperature_conversion():
    correct_temp = EQUIVALENT_TEMPERATURES[0]
    for temp in EQUIVALENT_TEMPERATURES[1]:
        step = Dry(vessel="filter", temp=temp)
        assert step.temp == correct_temp


@pytest.mark.chemputer
def test_time_conversion():
    correct_time = EQUIVALENT_TIMES[0]
    for time in EQUIVALENT_TIMES[1]:
        step = Dry(vessel="filter", time=time)
        assert step.time == correct_time


@pytest.mark.unit
def test_molecular_weight_conversion():
    correct_weight = EQUIVALENT_MOLECULAR_WEIGHTS[0]
    for weight in EQUIVALENT_MOLECULAR_WEIGHTS[1]:
        r = Reagent("water", molecular_weight=weight)
        assert r.molecular_weight == correct_weight


@pytest.mark.unit
def test_concentration_conversion():
    correct_conc = EQUIVALENT_CONCENTRATIONS[0]
    for conc in EQUIVALENT_CONCENTRATIONS[1]:
        r = Reagent("acid", concentration=conc)
        assert r.concentration == correct_conc


@pytest.mark.unit
def test_density_conversion():
    correct_density = EQUIVALENT_DENSITIES[0]
    for density in EQUIVALENT_DENSITIES[1]:
        r = Reagent("lead", density=density)
        assert r.density == correct_density
