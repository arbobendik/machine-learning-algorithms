# This class was created by Bendik Arbogast at the 23.10.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
from Pattern import Pattern
from classification_library import Classification_Library


class Pattern_Library:
    residual_pattern: list = []
    residual_group: list = []
    residual_group_precision: list = []

    @staticmethod
    def look_for_patterns(regression, xs) -> Pattern:
        # get pattern tolerance and regression curve coefficients from regression object
        classification = Classification_Library()
        res = classification.group_in_classes(xs, regression.residuals, regression.standard_deviation)
        group_pattern = res[0]
        groups: list = res[1]
        precision = res[2]
        new_groups = classification.sort_group(groups)
        new_pattern = classification.new_pattern(groups, new_groups, group_pattern)
        return Pattern(new_pattern, new_groups, precision)

    @staticmethod
    def __get_point_on_list(ns, n) -> float:
        ns.append(ns[0])
        ca = ((int(n) - int(n + 1)) ** 2 + (ns[int(n)] - ns[int(n + 1)]) ** 2) ** 0.5
        return ns[int(n)] + ca * (n % 1)
