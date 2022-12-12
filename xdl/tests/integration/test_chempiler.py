import os
import pytest

from ..utils import generic_chempiler_test

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, 'files')

@pytest.mark.integration
def test_lidocaine():
    generic_chempiler_test(
        os.path.join(FOLDER, 'lidocaine.xdl'),
        os.path.join(FOLDER, 'lidocaine_graph.json')
    )

@pytest.mark.integration
def test_dmp():
    generic_chempiler_test(
        os.path.join(FOLDER, 'DMP.xdl'),
        os.path.join(FOLDER, 'DMP_graph.json')
    )

@pytest.mark.integration
def test_alkyl_fluor():
    generic_chempiler_test(
        os.path.join(FOLDER, 'AlkylFluor.xdl'),
        os.path.join(FOLDER, 'AlkylFluor_graph.graphml')
    )

@pytest.mark.integration
def test_orgsyn_v83p0184a():
    generic_chempiler_test(
        os.path.join(FOLDER, 'orgsyn_v83p0184a.xdl'),
        os.path.join(FOLDER, 'orgsyn_v83p0184a_graph.json')
    )

@pytest.mark.integration
def test_orgsyn_v83p0193():
    generic_chempiler_test(
        os.path.join(FOLDER, 'orgsyn_v83p0193.xdl'),
        os.path.join(FOLDER, 'orgsyn_v83p0193_graph.json')
    )

@pytest.mark.integration
def test_orgsyn_v80p0129():
    generic_chempiler_test(
        os.path.join(FOLDER, 'orgsyn_v80p0129.xdl'),
        os.path.join(FOLDER, 'orgsyn_v80p0129_graph.json')
    )

@pytest.mark.integration
def test_orgsyn_v88p0152_a():
    generic_chempiler_test(
        os.path.join(FOLDER, 'orgsyn_v88p0152_a.xdl'),
        os.path.join(FOLDER, 'orgsyn_v88p0152_a_graph.json')
    )

@pytest.mark.integration
def test_orgsyn_v81p0262():
    generic_chempiler_test(
        os.path.join(FOLDER, 'orgsyn_v81p0262.xdl'),
        os.path.join(FOLDER, 'orgsyn_v81p0262_graph.json')
    )

@pytest.mark.integration
def test_orgsyn_v87p0016():
    generic_chempiler_test(
        os.path.join(FOLDER, 'orgsyn_v87p0016.xdl'),
        os.path.join(FOLDER, 'orgsyn_v87p0016_graph.json')
    )

@pytest.mark.integration
def test_orgsyn_v90p0251():
    generic_chempiler_test(
        os.path.join(FOLDER, 'orgsyn_v90p0251.xdl'),
        os.path.join(FOLDER, 'orgsyn_v90p0251_graph.json')
    )
