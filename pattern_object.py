# This class was created by Bendik Arbogast at the 27.10.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
class Pattern_Object:
    residual_pattern: list = []
    residual_group: list = []
    residual_group_precision: list = []

    def __init__(self, residual_pattern, residual_group, residual_group_precision):
        self.residual_pattern = residual_pattern
        self.residual_group = residual_group
        self.residual_group_precision = residual_group_precision
