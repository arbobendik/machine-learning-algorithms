# This class was created by Bendik Arbogast at the 14.11.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
from Neuron import Neuron
import sqlite3
import json


class Database:
    name: str

    def __init__(self, name: str):
        # establish connection
        connection = sqlite3.connect(name)
        cursor = connection.cursor()
        # save name as attribute
        self.name = name
        # create Neuron object table
        sql_query = """
        CREATE TABLE IF NOT EXISTS neurons (
        pointers_address VARCHAR,
        pointers VARCHAR,
        address VARCHAR
        );"""
        cursor.execute(sql_query)
        connection.commit()

    def set_neuron(self, neuron: Neuron):
        # establish connection
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        # save object attributes as locals and convert lists to json to store them in the database
        pointers_addresses = json.dumps(neuron.pointers_addresses)
        pointers_thresholds = json.dumps(neuron.pointers_thresholds)
        address = neuron.address
        # make the data ready for the database
        db_neuron = [pointers_addresses, pointers_thresholds, address]
        cursor.execute("INSERT INTO neurons VALUES (?, ?, ?)", db_neuron)
        connection.commit()

    def delete_neuron(self, address):
        # establish connection
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM neurons WHERE address=?", (address,))
        connection.commit()

    def get_neuron(self, address) -> Neuron:
        # establish connection
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM neurons WHERE address=?", (address, ))
        db_neuron = cursor.fetchall()[0]
        # convert json strings to lists
        pointers_address = json.loads(db_neuron[0])
        pointers_thresholds = json.loads(db_neuron[1])
        address = db_neuron[2]
        connection.commit()
        # package fetched data in Neuron
        return Neuron(pointers_address, pointers_thresholds, address)
