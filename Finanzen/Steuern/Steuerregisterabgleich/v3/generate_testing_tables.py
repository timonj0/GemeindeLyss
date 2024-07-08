'''Table Generator for testing the Steuerregisterabgleich v3'''
import pandas
# Create some tables for testing. Table columns are: ["NameEinwohner", "AlleVornamen", "Geburtsdatum", "StrasseHaus", "PLZOrt", "Verischertennummer", "Zuzug_Datum"]. Come up with some data yourself.

# Create an array of arrays with the data
data1 = [
    ["Max Mustermann", "Max", "01.01.1990", "Musterstraße 1",
        "12345 Musterstadt", "123456789", "01.01.2022"],
    ["Erika Mustermann", "Erika", "01.01.1991", "Musterstraße 2",
        "12345 Musterstadt", "123456790", "01.01.2022"],
    ["Hans Müller", "Hans", "01.01.1992", "Musterstraße 3",
        "12345 Musterstadt", "123456791", "01.01.2022"],
    ["Anna Schmidt", "Anna", "01.01.1993", "Musterstraße 4",
        "12345 Musterstadt", "123456792", "01.01.2022"],
    ["Peter Schmitt", "Peter", "01.01.1994", "Musterstraße 5",
        "12345 Musterstadt", "123456793", "01.01.2022"],
    ["Laura Müller", "Laura", "01.01.1995", "Musterstraße 6",
        "12345 Musterstadt", "123456794", "01.01.2022"],
    ["Markus Schmidt", "Markus", "01.01.1996", "Musterstraße 7",
        "12345 Musterstadt", "123456795", "01.01.2022"],
    ["Sabine Meier", "Sabine", "01.01.1997", "Musterstraße 8",
        "12345 Musterstadt", "123456796", "01.01.2022"],
    ["Thomas Wagner", "Thomas", "01.01.1998", "Musterstraße 9",
        "12345 Musterstadt", "123456797", "01.01.2022"],
    ["Julia Becker", "Julia", "01.01.1999", "Musterstraße 10",
        "12345 Musterstadt", "123456798", "01.01.2022"],
    ["John Doe", "John", "01.01.2024", "Musterstraße 11",
        "12345 Musterstadt", "123456799", "01.01.2024"],
    ["Jane Smith", "Jane", "01.01.2025", "Musterstraße 12",
        "12345 Musterstadt", "123456800", "01.01.2024"],
    ["Michael Johnson", "Michael", "01.01.2026", "Musterstraße 13",
        "12345 Musterstadt", "123456801", "01.01.2024"],
    ["Emily Davis", "Emily", "01.01.2027", "Musterstraße 14",
        "12345 Musterstadt", "123456802", "01.01.2024"],
    ["David Wilson", "David", "01.01.2028", "Musterstraße 15",
        "12345 Musterstadt", "123456803", "01.01.2024"],
    ["Sophia Anderson", "Sophia", "01.01.2029", "Musterstraße 16",
        "12345 Musterstadt", "123456804", "01.01.2024"],
    ["Oliver Martinez", "Oliver", "01.01.2030", "Musterstraße 17",
        "12345 Musterstadt", "123456805", "01.01.2024"],
    ["Emma Taylor", "Emma", "01.01.2031", "Musterstraße 18",
        "12345 Musterstadt", "123456806", "01.01.2024"],
    ["Daniel Brown", "Daniel", "01.01.2032", "Musterstraße 19",
        "12345 Musterstadt", "123456807", "01.01.2024"],
    ["Mia Miller", "Mia", "01.01.2033", "Musterstraße 20",
        "12345 Musterstadt", "123456808", "01.01.2024"],
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
