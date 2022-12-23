from typing import Any, Tuple

import numpy as np
import pandas as pd

from .utils.xdl_base import XDLBase


class Variable(XDLBase):
    """Abstract process variable class.

    TODO: Make sure __init__ rejects ``id``s that contain ``.``s.
    This is because the ``.`` is reserved for accessing tuple
    indices and dictionary entries of non-scalar generated values.
    """

    def generate(self):
        pass

    def feedback(self, point, value):
        pass


class ConstantVariable(Variable):
    """Generate a constant process variable.

    Properties:
        id (str): Variable id, used when binding process variables.
        value (Any): Constant value generated when the `generate()` method
            is called.
    """

    PROP_TYPES = {"id": str, "value": Any}

    def __init__(
        self,
        id: str,  # noqa: A002
        value: Any,
    ):
        """Args:
        value: Constant process variable value to return in the future.
        """
        super().__init__(locals())
        self.value = value

    def generate(self):
        return self.value


class RandomSimplexVariable(Variable):
    """Randomly sample a series of random numbers a_1, a_2, ..., a_N from a
    simplex, i.e. a_1 + a_2 + ... + a_N is a given constant total value.

    Under the hood, this class uses a Dirichlet distribution with adjustable
    concentration parameter, alpha.

    Properties:
        id (str): Variable id, used when binding process variables.
        nvars (int): The number of points in each sample, that is the
            length, N, of the returned vector (a_1, a_2, ..., a_N).
        total(float): The constant sum of a_1 + a_2 + ... + a_N.
        alpha (float): Concentration parameter for the Dirichlet distribution.
        limits (tuple of floats): (low, high) limits for the generated numbers.
    """

    PROP_TYPES = {
        "id": str,
        "nvars": int,
        "total": float,
        "alpha": float,
    }

    def __init__(
        self,
        id: str,  # noqa: A002
        nvars: int,
        total: float,
        alpha: float,
        limits: tuple = (0.1, 10),
    ):
        super().__init__(locals())
        self.limits = limits
        self.alphas = np.array([self.alpha] * self.nvars)

    def generate(self):
        while True:
            generated_values = self.total * np.random.dirichlet(self.alphas)
            for generated_value in generated_values:
                if generated_value < self.limits[0] or generated_value > self.limits[1]:
                    continue
            return generated_values


class FunctionVariable(Variable):
    pass


class ExponentialVariable(FunctionVariable):
    """Generate a finite sequence of single values where the first generated
    value ``a[0] = start``; the last ``a[n_points] = stop``, and ``a[i]/a[i-1]``
    is a constant.

    Properties:
        id (str): Variable id, used when binding process variables.
        start (float): First value (``a[0]``).
        stop (float): Last value (``a[n_points]``).
        n_points (int): Number of datapoints generated.
    """

    PROP_TYPES = {
        "id": str,
        "start": float,
        "stop": float,
        "n_points": int,
    }

    def __init__(
        self,
        id: str,  # noqa: A002
        start: float,
        stop: float,
        n_points: int,
    ):
        super().__init__(locals())
        self.points = np.geomspace(self.start, self.stop, self.n_points)
        self.state = self.points.__iter__()

    def generate(self):
        return next(self.state)


class LinearVariable(FunctionVariable):
    """Generate a finite sequence of single values where the first generated
    value ``a[0] = start``; the last ``a[n_points] = stop``, and
    ``a[i] - a[i-1]`` is a constant.

    Properties:
        id (str): Variable id, used when binding process variables.
        start (float): First value (`a[0]`).
        stop (float): Last value (`a[n_points]`).
        n_points (int): Number of datapoints generated.
    """

    PROP_TYPES = {  # noqa: A002
        "id": str,
        "start": float,
        "stop": float,
        "n_points": int,
    }

    def __init__(
        self,
        id: str,  # noqa: A002
        start: float,
        stop: float,
        n_points: int,
    ):
        super().__init__(locals())
        self.points = np.linspace(self.start, self.stop, num=self.n_points)
        self.state = self.points.__iter__()

    def generate(self):
        return next(self.state)


class OscillatingVariable(FunctionVariable):
    """Generate a infinite sequence of single values where the ith generated
    value is ``a[i] = amplitude * sin(init_phase + increment * i)``. Note that
    generated points that lie outside low and high limits in ``limit`` are
    discarded.

    Properties:
        id (str): Variable id, used when binding process variables.
        amplitude (float): Amplitude of the generated oscillating wave.
        init_phase (float): Phase of the first generated value,
            subject to limits.
        increment (float): Increase in phase in each successive generated
            value.
        limits (tuple of floats): (low, high) limits for the generated numbers.
    """

    PROP_TYPES = {
        "id": str,
        "increment": float,
        "init_phase": float,
        "limit": tuple,
    }

    def __init__(
        self,
        id: str,  # noqa: A002
        amplitude: float,
        init_phase: float,
        increment: float,
        limit: Tuple[float, float] = (-10.0, 10.0),
    ):
        super().__init__(locals())
        self.state = self.init_phase - self.increment

    def generate(self):
        while True:
            self.state += self.increment
            return_value = np.sin(self.state)
            if return_value < self.limit[0] or return_value > self.limit[1]:
                continue
            return np.sin(self.state)


class TableVariable(Variable):
    """Generate rows (as dictionaries) from a table.

    TODO: Implement path resolution mechanism. Currently need to use absolute
    path or rely on Python being run from the correct working directory.

    Properties:
        id (str): Variable id, used when binding process variables.
        csv_file (float): Amplitude of the generated oscillating wave.
    """

    PROP_TYPES = {
        "id": str,
        "csv_file": str,
    }

    def __init__(
        self,
        id: str,  # noqa: A002
        csv_file: str,
    ):
        super().__init__(locals())
        self.df = pd.read_csv(csv_file)
        self.state = self.df.iterrows()
        self._csv = csv_file

    def generate(self):
        _, row = next(self.state)
        return dict(row)


class GaussianProcess(Variable):
    pass
