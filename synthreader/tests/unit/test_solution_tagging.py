import pytest
from synthreader.tagging import tag_synthesis
from synthreader.words import SolutionWord, ReagentGroupWord

SOLUTIONS = [
    # DMP Step 3 (menthol change to NaOH)
    {
        'text': 'A solution of NaOH (31.25 g in 500 mL DCM)',
        'solutes': {'NaOH (31.25 g in 500 mL DCM)': '31.25 g'},
        'solvent': {'name': 'DCM', 'volume': '500 mL'}
    },
    # DMP Step 1
    {
        'text': 'a solution of Oxone (181.0 g, 0.29 mol, 1.3 equiv) in deionized water (650 mL, 0.45 M)',
        'solutes': {'oxone': '181.0 g'},
        'solvent': {'name': 'deionized water', 'volume': '650 mL'}
    # Made up
    },
]

def test_solution_word(word, solution):
    assert (word.solvent.name.lower()
            == solution['solvent']['name'].lower())
    assert (str(word.solvent.volume).lower()
            == solution['solvent']['volume'].lower())
    for solute in word.solutes:
        print(str(solute.mass))
        assert solute.name in solution['solutes']
        assert (str(solute.mass).lower()
                == solution['solutes'][solute.name].lower())

@pytest.mark.unit
def test_solution_tagging():
    for solution in SOLUTIONS:
        tagged_synthesis = tag_synthesis(solution['text'])
        found_solution = False
        for sentence in tagged_synthesis:
            for word in sentence:
                if type(word) == SolutionWord:
                    found_solution = True
                    test_solution_word(word, solution)

                elif type(word) == ReagentGroupWord:
                    for subword in word.reagents:
                        if type(subword) == SolutionWord:
                            test_solution_word(subword, solution)
                            found_solution = True
        assert found_solution
