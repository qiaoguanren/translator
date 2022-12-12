import pytest
from xdl.errors import XDLValueError
from xdl.reagents import Reagent

@pytest.mark.unit
def test_reagent_roles():
    with pytest.raises(XDLValueError):
        Reagent(id="irnbru", role="juice")
    Reagent(id="DCM", role="solvent")
    Reagent(id="Pd(DBA)2", role="catalyst")
    Reagent(id="2-aminophenethyl alcohol", role="reagent")
    Reagent(id="compound 2", role="substrate")
