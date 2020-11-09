# This class was created by Bendik Arbogast at the 27.10.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
from typing import Callable


class Regression_Object:
    factors: list = []
    residuals: list = []
    formula: Callable[[float], float] = lambda x: 0
    standard_deviation: float = 0.0
    precision: float = 0.0

    def __int__(self):
        pass

    def __init__(self, factors, residuals, formula, standard_deviation, precision):
        self.factors = factors
        self.residuals = residuals
        self.standard_deviation = standard_deviation
        self.formula = formula
        self.precision = precision
