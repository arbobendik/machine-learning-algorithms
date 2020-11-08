# This class was created by Bendik Arbogast at the 23.10.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
from pattern_object import Pattern_Object


class Pattern_Library:

    residual_pattern: list = []
    residual_group: list = []
    residual_group_precision: list = []

    def look_for_patterns(self, regression_obj, xs) -> Pattern_Object:
        # get pattern tolerance and regression curve coefficients from regression object
        res = regression_obj.residuals
        t = regression_obj.tolerance
        res = self.group(xs, res, t)
        groups = res[1]
        group_pattern = res[0]
        # later the model should use trained, known patterns to describe the residual_pattern
        precision = res[4]
        return Pattern_Object(group_pattern, groups, precision)

    @staticmethod
    def __get_point_on_list(ns, n) -> float:
        ns.append(ns[0])
        ca = ((int(n) - int(n + 1)) ** 2 + (ns[int(n)] - ns[int(n + 1)]) ** 2) ** 0.5
        return ns[int(n)] + ca * (n % 1)
