# SynthReader

This repository is for converting chemical synthesis procedure texts to XDL.

## Usage
```
from synthreader import text_to_xdl

s = 'MeCN (50 mL) was added to...'

xdl = text_to_xdl(s)
xdl.save('procedure.xdl')
```

## Installation

```
git clone http://datalore.chem.gla.ac.uk/Chemputer/synthreader.git
cd synthreader
pip install -e .
python postinstall.py
```

## Updating
```
cd synthreader
git pull origin master
```

## Development

When developing SynthReader the following development strategy MUST be followed, otherwise the project is guaranteed to fail.

1. Take procedure from the literature and convert it to XDL with SynthReader.

2. Make a list of all the mistakes that are made in the conversion.

3. Branch off dev into a fix branch, with the name of the procedure you are working on.

4. For every mistake noted in step 2:

    1. Add patterns to SynthReader tagging, or make other alterations to the algorithm to make it work.
    2. Add a test for the procedure.
    ```
    from tests.integration.generator import generate_test_info
    s = 'MeCN (50 mL) was added to...'
    generate_test_info(s, 'procedure_name', 'tests/integration/test_info/procedure_name.py')
    ```
    2. Make sure all tests still pass: `pytest tests/all_tests.py -m "fast_integration" -rf`
    3. If any tests fail, make further changes so that the tests pass.
    4. `git rebase -i dev` to clean up commit history.

5. Run all tests a final time and make do any final commits/rebasing.

6. Merge the branch back into dev (ONLY if all tests pass).
