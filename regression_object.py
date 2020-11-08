# This class was created by Bendik Arbogast at the 27.10.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
from typing import Callable


class Regression_Object:
    residuals: list = []
    tolerance: float = 0.0
    formula: Callable[[float, float], float] = lambda x: x
    factors: list = []

    def __init__(self, residuals, tolerance, formula, factors):
        self.residuals = residuals
        self.tolerance = tolerance
        self.formula = formula
        self.factors = factors
