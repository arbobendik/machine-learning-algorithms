# This class was created by Bendik Arbogast at the 08.11.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
import copy
import functools
from regression_library import Regression_Library


class Classification_Library:
    @staticmethod
    def group_in_classes(ns: list, ms: list, t: float) -> list:
        # sort variables in exclusive groups and exclude border areas to prevent overlapping (group averages)
        exclusive_groups: list = []
        # use inclusive groups to collect and group the ignored values afterwards (group averages)
        inclusive_groups: list = []
        # list of inclusive and exclusive groups in the form of average group values
        groups: list = []
        # collect all corresponding x and y values to the groups created above
        groups_xs: list = []
        groups_ys: list = []
        # create an artificial precision metric
        groups_precision: list = []
        # save group repetition pattern to detect patterns in the order of the grouped elements
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
                    reg = Regression_Library(groups_xs[gi], groups_ys[gi]).get_flat()
                    # save new calculated average value of group
                    exclusive_groups[i] = reg.factors[0]
                    groups[gi] = reg.factors[0]
                    # save precision of calculation of average value
                    groups_precision[gi] = 1 / ((sum([abs(r) for r in reg.residuals]) / (max(ns) - min(ns))) + 1)
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
                        reg = Regression_Library(groups_xs[gy], groups_ys[gy]).get_flat()
                        # save new calculated average value of group
                        inclusive_groups[y] = reg.factors[0]
                        groups[gy] = reg.factors[0]
                        # save precision of calculation of average value
                        groups_precision[gy] = 1 / (
                                (sum([abs(r) for r in reg.residuals]) / (max(ns) - min(ns))) + 1)
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
                group_pattern[1].append(len(groups) - 1)
        return [group_pattern, groups, groups_precision]

    @staticmethod
    def sort_group(unsorted_groups: list) -> list:
        # sort groups by their values
        new_groups: list = []
        old_groups: list = copy.deepcopy(unsorted_groups)
        for i in range(0, len(unsorted_groups)):
            mini = min(old_groups)
            new_groups.append(mini)
            old_groups.remove(mini)
        return new_groups

    @staticmethod
    def new_pattern(groups, ngs, pgs) -> list:
        dictionary: list = []
        for i in range(0, len(groups)):
            match = functools.reduce(lambda n, ng: ng if groups[i] == ngs[ng] else n, range(0, len(ngs)))
            dictionary.append(match)
        return [pgs[0], [dictionary[ps] for ps in pgs[1]]]
