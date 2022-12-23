import pytest

from xdl.errors import XDLFailedPropLimitError
from xdl.reagents import Reagent


@pytest.mark.unit
def test_density_prop_limits():
    d_prop1 = Reagent("water", density="4.2 g/mL")
    d_prop2 = Reagent("acetone", density="55.2 g/cm3")
    d_prop3 = Reagent("dcm", density="2 g/ml")

    assert d_prop1.density == 4.2
    assert d_prop2.density == 55.2
    assert d_prop3.density == 2

    with pytest.raises(XDLFailedPropLimitError):
        Reagent("glue", density="1.5 g/cm2")
        Reagent("methanol", density="2.98 g/cm4")
        Reagent("rotaxane", density="-12.2 g/mL")


@pytest.mark.unit
def test_molecular_formula_prop_limits():
    Reagent("water", molecular_formula="H2O")
    Reagent("ethanol", molecular_formula="c2H5oH")
    Reagent("methane", molecular_formula="ch4")

    with pytest.raises(XDLFailedPropLimitError):
        Reagent("butane", molecular_formula="c4-H10")
        Reagent("propane", molecular_formula="12-32&*^29###")


@pytest.mark.unit
def test_molecular_weight_prop_limits():
    r1 = Reagent("water", molecular_weight="18 g/mol")
    r2 = Reagent("methane", molecular_weight="16 g/mol")

    assert r1.molecular_weight == 18
    assert r2.molecular_weight == 16

    with pytest.raises(XDLFailedPropLimitError):
        Reagent("ethane", molecular_weight="-13.2312 g/mol")
        Reagent("glue", molecular_weight="30 g/MOL")


@pytest.mark.unit
def test_concentration_prop_limit():
    r1 = Reagent("water", concentration="4.0 mol/L")
    r2 = Reagent("sulfuric acid", concentration="12.5 mol/l")

    assert r1.concentration == 4.0
    assert r2.concentration == 12.5

    with pytest.raises(XDLFailedPropLimitError):
        Reagent("hydrochloric acid", concentration=".5 mool/l")
        Reagent("phosphoric acid", concentration="2.5 MOL/L")
        Reagent("ntiric acid", concentration="-44 mol/L")
        Reagent("ntiric acid", concentration="-420.69 mol/l")


@pytest.mark.unit
def test_reagent_solid():
    for liquid in ["h2o", "sulfuric acid", "benzene"]:
        for concentration in ["38.9 mol/L", "2 mol/L", "1.23 mmol/L"]:
            reagent = Reagent(name=liquid, concentration=concentration)
            assert reagent.solid is False

    for solid in ["chalcopyrite", "clay", "nacl"]:
        reagent = Reagent(name=solid, solid=True)
        assert reagent.solid is True
