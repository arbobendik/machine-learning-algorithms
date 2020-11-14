# This class was created by Bendik Arbogast at the 08.11.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
class Neuron:
    pointers_address: list = []
    pointers_thresholds: list = []
    address: int

    def __init__(self, pointers_address, pointers_thresholds, address):
        self.pointers_address = pointers_address
        self.pointers_thresholds = pointers_thresholds
        self.address = address
