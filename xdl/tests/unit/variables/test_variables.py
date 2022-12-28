from os import path

import pytest

from xdl.variables import ExponentialVariable, LinearVariable, TableVariable


def assert_approx_eq(tol):
    def inner(x, y):
        assert abs(x - y) < tol

    return inner


@pytest.mark.unit
def test_linear_variable():
    assertfn = assert_approx_eq(1e-5)

    test1 = LinearVariable(id="test1", start=1, stop=3, n_points=3)
    assertfn(test1.generate(), 1)
    assertfn(test1.generate(), 2)
    assertfn(test1.generate(), 3)

    test2 = LinearVariable(id="test2", start=2, stop=8, n_points=4)
    assertfn(test2.generate(), 2)
    assertfn(test2.generate(), 4)
    assertfn(test2.generate(), 6)
    assertfn(test2.generate(), 8)

    with pytest.raises(StopIteration):
        test2.generate()


@pytest.mark.unit
def test_exponential_variable():
    assertfn = assert_approx_eq(1e-5)

    test1 = ExponentialVariable(id="test1", start=1, stop=100, n_points=3)
    assertfn(test1.generate(), 1)
    assertfn(test1.generate(), 10)
    assertfn(test1.generate(), 100)

    test2 = ExponentialVariable(id="test2", start=2, stop=8, n_points=3)
    assertfn(test2.generate(), 2)
    assertfn(test2.generate(), 4)
    assertfn(test2.generate(), 8)

    with pytest.raises(StopIteration):
        test2.generate()


@pytest.mark.unit
def test_table_variable():
    csv_file = path.join(path.dirname(__file__), "table_variables_eg.csv")
    test_variables = TableVariable(id="table", csv_file=csv_file).generate()

    assert list(test_variables.keys()) == ["reagent", "volume"]
    assert list(test_variables.values()) == ["reagent_1", 4]
