# This class was created by Bendik Arbogast at the 14.11.2020 and is available free of charge to the general public.
# All rights reserved. If you have any questions or ideas to improve the contents of this file
# please consider writing an email to arbobendik@gmail.com or contact me on GitHub.
from Neuron import Neuron
import sqlite3


class Database:
    def __init__(self,):

verbindung = sqlite3.connect("neural_net.db")
zeiger = verbindung.cursor()

sql_anweisung = """
CREATE TABLE IF NOT EXISTS adressen (
vorname VARCHAR(20), 
nachname VARCHAR(30), 
geburtstag DATE
);"""

zeiger.execute(sql_anweisung)


beruehmtheiten = [('Georg Wilhelm Friedrich', 'Hegel', '27.08.1770'),
                  ('Johann Christian Friedrich', 'Hölderlin', '20.03.1770'),
                  ('Rudolf Ludwig Carl', 'Virchow', '13.10.1821')]

zeiger.executemany("""
                INSERT INTO personen 
                       VALUES (?,?,?)
                """, beruehmtheiten)

zeiger.execute(sql_anweisung)
nachname   = "Schiller"
vorname    = "Johann Christoph Friedrich"

zeiger.execute("UPDATE personen SET vorname=? WHERE nachname=?", (vorname, nachname))
verbindung.commit()
zeiger.execute("SELECT vorname FROM personen WHERE vorname=?", ('*',))
inhalt = zeiger.fetchall()
print(inhalt)
verbindung.close()