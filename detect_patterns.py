# This class was created by Bendik Arbogast at the 23.10.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.



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
    def group(ns, ms, t) -> list:
        exclusive_groups: list = []
        inclusive_groups: list = []
        groups: list = []
        groups_xs: list = []
        groups_ys: list = []
        groups_precision: list = []
        group_pattern: list = [[], []]
        for r in range(0, len(ms)):
            build_new_exclusive_group: bool = True
            inclusive: bool = False
            for i in range(0, len(exclusive_groups)):
                # test if y is in the range of 0.5 times of the tolerance next to the average of any group
                if exclusive_groups[i] - t * 0.5 < ms[r] < exclusive_groups[i] + t * 0.5:
                    group_pattern[0].append(ns[r])
                    gi = i
                    for it in range(i, len(groups)):
                        if groups[it] == exclusive_groups[i]:
                            gi = it
                            break
                    group_pattern[1].append(gi)
                    groups_xs[gi].append(ns[r])
                    groups_ys[gi].append(ms[r])
                    this_regression = Reg(groups_xs[gi], groups_ys[gi]).get_flat()
                    # save new calculated average value of group
                    exclusive_groups[i] = this_regression[3][0]
                    groups[gi] = this_regression[3][0]
                    # save precision of calculation of average value
                    groups_precision[gi] = 1 / ((sum([abs(r) for r in this_regression[2]]) / (max(ns) - min(ns))) + 1)
                    build_new_exclusive_group = False
                # test if y is in the range of the tolerance next to the average of any group
                # to prevent groups from overlapping
                if exclusive_groups[i] - t < ms[r] < exclusive_groups[i] + t:
                    inclusive = True
            if inclusive and build_new_exclusive_group:
                build_new_inclusive_group: bool = True
                for y in range(0, len(inclusive_groups)):
                    # test if y is in the range of 0.5 times of the tolerance next to the average of any group
                    if inclusive_groups[y] - t * 0.5 < ms[r] < inclusive_groups[y] + t * 0.5:
                        group_pattern[0].append(ns[r])
                        gy = y
                        for it in range(y, len(groups)):
                            if groups[it] == inclusive_groups[y]:
                                gy = it
                                break
                        group_pattern[1].append(gy)
                        groups_xs[gy].append(abs(ns[r]))
                        groups_ys[gy].append(ms[r])
                        this_regression = Reg(groups_xs[gy], groups_ys[gy]).get_flat()
                        # save new calculated average value of group
                        inclusive_groups[y] = this_regression[3][0]
                        groups[gy] = this_regression[3][0]
                        # save precision of calculation of average value
                        groups_precision[gy] = 1 / (
                                (sum([abs(r) for r in this_regression[2]]) / (max(ns) - min(ns))) + 1)
                        build_new_inclusive_group = False
                if build_new_inclusive_group:
                    inclusive_groups.append(ms[r])
                    groups.append(ms[r])
                    groups_xs.append([ns[r]])
                    groups_ys.append([ms[r]])
                    groups_precision.append(0)
                    group_pattern[0].append(ns[r])
                    group_pattern[1].append(len(groups) - 1)
            elif build_new_exclusive_group:
                exclusive_groups.append(ms[r])
                groups.append(ms[r])
                groups_xs.append([ns[r]])
                groups_ys.append([ms[r]])
                groups_precision.append(0)
                group_pattern[0].append(ns[r])
                group_pattern[1].append(len(groups)-1)
        return [group_pattern, groups, groups_xs, groups_ys, groups_precision]

    @staticmethod
    def __get_point_on_list(ns, n) -> float:
        ns.append(ns[0])
        ca = ((int(n) - int(n + 1)) ** 2 + (ns[int(n)] - ns[int(n + 1)]) ** 2) ** 0.5
        return ns[int(n)] + ca * (n % 1)
