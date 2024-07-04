'''Table Generator for testing the Steuerregisterabgleich v3'''
import pandas
# Create some tables for testing. Table columns are: ["NameEinwohner", "AlleVornamen", "Geburtsdatum", "StrasseHaus", "PLZOrt", "Verischertennummer", "Zuzug_Datum"]. Come up with some data yourself.

# Create an array of arrays with the data
data1 = [
    ["Max Mustermann", "Max", "01.01.1990", "Musterstraße 1",
        "12345 Musterstadt", "123456789", "01.01.2023"],
    ["Erika Mustermann", "Erika", "01.01.1991", "Musterstraße 2",
        "12345 Musterstadt", "123456790", "01.01.2023"],
    ["Hans Müller", "Hans", "01.01.1992", "Musterstraße 3",
        "12345 Musterstadt", "123456791", "01.01.2023"],
    ["Anna Schmidt", "Anna", "01.01.1993", "Musterstraße 4",
        "12345 Musterstadt", "123456792", "01.01.2023"],
    ["Peter Schmitt", "Peter", "01.01.1994", "Musterstraße 5",
        "12345 Musterstadt", "123456793", "01.01.2023"],
    ["Laura Müller", "Laura", "01.01.1995", "Musterstraße 6",
        "12345 Musterstadt", "123456794", "01.01.2023"],
    ["Markus Schmidt", "Markus", "01.01.1996", "Musterstraße 7",
        "12345 Musterstadt", "123456795", "01.01.2023"],
    ["Sabine Meier", "Sabine", "01.01.1997", "Musterstraße 8",
        "12345 Musterstadt", "123456796", "01.01.2023"],
    ["Thomas Wagner", "Thomas", "01.01.1998", "Musterstraße 9",
        "12345 Musterstadt", "123456797", "01.01.2023"],
    ["Julia Becker", "Julia", "01.01.1999", "Musterstraße 10",
        "12345 Musterstadt", "123456798", "01.01.2023"],

]

# Table 1: first 7 rows ONLY
table1 = pandas.DataFrame(data1[:7], columns=["NameEinwohner", "AlleVornamen",
                          "Geburtsdatum", "StrasseHaus", "PLZOrt", "Verischertennummer", "Zuzug_Datum"])

# Table 2: all rows
table2 = pandas.DataFrame(data1, columns=["NameEinwohner", "AlleVornamen",
                          "Geburtsdatum", "StrasseHaus", "PLZOrt", "Verischertennummer", "Zuzug_Datum"])

# Export the tables as Excel files
table1.to_excel("table1_0_to_7.xlsx", index=False)
table2.to_excel("table2_all.xlsx", index=False)
