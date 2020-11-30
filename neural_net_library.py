# This class was created by Bendik Arbogast at the 25.11.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
from Neuron import Neuron
from Database import Database


class Neural_Net_Library:
    def __init__(self, width: int, height: int, name: str):
        db = Database(name)
        thresholds = [1] * height
        for wi in range(0, width):
            address_pointers = [str(wi + 1) + "|" + str(a) for a in range(height)]
            for he in range(0, height):
                neuron = Neuron(address_pointers, thresholds, str(wi) + "|" + str(he))
                db.set_neuron(neuron)

    def train(self, dataset_x, dataset_y):
        pass
