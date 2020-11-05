# This class was created by Bendik Arbogast at the 27.10.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.

from typing import Callable
from regression_object import Regression_Object
from pattern_object import Pattern_Object
from regression_system import Regression_Library
from detect_patterns import Pattern_Library


class Prediction_Model:
    xs: list = []
    ys: list = []

    def __init__(self, x_values, y_values):
        self.xs = x_values
        self.ys = y_values
        self.regression = []

    def get_regression_object(self) -> Regression_Object:
        reg = Regression_Library(self.xs, self.ys).fit()
        # create new Regression_Object and append specific information
        t = sum([abs(r) for r in reg[2]]) / len(reg[2])
        if reg[0] == 2:
            formula: Callable[[float, float], float] = lambda x, p: (reg[3][2]*x**2+reg[3][1]*x+reg[3][0])+p
            factors = [reg[3][0], reg[3][1], reg[3][2]]
        elif reg[0] == 1:
            formula: Callable[[float, float], float] = lambda x, p: (x*reg[3][1]+reg[3][0])+p
            factors = [reg[3][0], reg[3][1]]
        else:
            formula: Callable[[float, float], float] = lambda x, p: (reg[3][0])+p
            factors = [reg[3][0]]
        # return created Regression_Object
        return Regression_Object(reg[2], t, formula, factors)

    def get_pattern_object(self, regression_obj) -> Pattern_Object:
        return Pattern_Library().look_for_patterns(regression_obj, self.xs)

    def predict(self, regression_obj: Regression_Object, pattern_obj: Pattern_Object, x) -> list:
        residual_pattern = pattern_obj.residual_pattern
        residual_group = pattern_obj.residual_group
        regression_formula = regression_obj.formula
        # determine which index of residual_group is used at x
        pat_reg = Regression_Library(residual_pattern[0], residual_pattern[1]).get_flat()
        pn = pat_reg[3][0] + x*pat_reg[3][1] + x**2*pat_reg[3][2]
        xs: list = [x] * len(residual_group)
        print(residual_group)
        print(xs)
        predicted_ys = list(map(regression_formula, xs, residual_group))
        print(predicted_ys)
        # get value of floating point indexes in residual_group and it's precision score
        precision = self.__get_point_on_list(pattern_obj.residual_group_precision, pn)
        y = self.__get_point_on_list(predicted_ys, pn)
        return [precision, y, predicted_ys]

    @staticmethod
    def __get_point_on_list(ns, n) -> float:
        ns.append(ns[0])
        ca = ((int(n) - int(n + 1)) ** 2 + (ns[int(n)] - ns[int(n + 1)]) ** 2) ** 0.5
        return ns[int(n)] + ca * (n % 1)
