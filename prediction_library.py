# This class was created by Bendik Arbogast at the 27.10.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
from typing import Callable
from regression_object import Regression_Object
from pattern_object import Pattern_Object
from regression_library import Regression_Library
from pattern_library import Pattern_Library


class Prediction_Library:
    xs: list = []
    ys: list = []

    def __init__(self, x_values, y_values):
        self.xs = x_values
        self.ys = y_values

    def get_regression_object(self) -> Regression_Object:
        # get best fitting regression by comparing precision and return it
        reg = Regression_Library(self.xs, self.ys)
        q = reg.get_quadratic()
        li = reg.get_linear()
        f = reg.get_flat()
        if li.precision <= q.precision and f.precision <= q.precision:
            return q
        elif f.precision <= li.precision:
            return li
        else:
            return f

    def get_pattern_object(self, regression_obj) -> Pattern_Object:
        return Pattern_Library().look_for_patterns(regression_obj, self.xs)

    def predict(self, regression_obj: Regression_Object, pattern_obj: Pattern_Object, x) -> list:
        residual_pattern = pattern_obj.residual_pattern
        residual_group = pattern_obj.residual_group
        # determine which index of residual_group is used at x
        pat_reg = Regression_Library(residual_pattern[0], residual_pattern[1]).get_flat()
        pn = pat_reg.formula(x)
        print(pn)
        xs: list = [x] * len(residual_group)
        predicted_ys = [regression_obj.formula(x) + r for r in residual_group]
        # get value of floating point indexes in residual_group and it's precision score
        precision = self.__get_point_on_list(pattern_obj.residual_group_precision, pn)
        y = self.__get_point_on_list(predicted_ys, pn)
        return [precision, y, predicted_ys]

    @staticmethod
    def __get_point_on_list(ns, n) -> float:
        # append first element of list, to prevent that ns[n+1] doesn't exist
        ns.append(ns[0])
        # calculate gradient between the two points around the desired x-value
        ca = ((ns[int(n)] - ns[int(n + 1)]) / (int(n) - int(n + 1)))
        # multiply the calculated deviation with the x-difference to the lower list point
        return ns[int(n)] + ca * (n % 1)
