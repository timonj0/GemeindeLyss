'''Steuerregisterabgleich v3.0'''
# Version 3.0: Interactive CLI tool
# Author: Timon Jakob
# Date: 07.2023

import os
import pandas

# HashMap to store the dataframes with the corresponding name
session_dataframes = {}


def load_table_from_excel(file_path: str) -> pandas.DataFrame:
    '''Load a table from an Excel file'''
    return pandas.read_excel(file_path)


def print_table_pretty(table: pandas.DataFrame):
    '''Prints a table in a pretty format'''
    print(table.to_string(index=False))


def print_help():
    '''Prints the help'''
    print("Hilfe:")
    print(" - 'help': Zeigt diese Hilfe an")
    print(" - 'quit': Beendet das Programm")
    print(" - 'load <excel/csv> <tabellenname> <dateiname>': Lädt eine Tabelle aus einer Excel- oder CSV-Datei.")
    print(" - 'show <tabellenname> <(anzahl)>': Zeigt die ersten n Zeilen der Tabelle an. Standardmäßig 5 Zeilen. 0 zeigt alle Zeilen an.")
    print(" - 'export': Exportiert die Daten")


def main_loop():
    '''Main loop of the program'''
    while True:
        inp = input(" > ").lower().split(" ")
        action = inp[0]
        args = inp[1:]

        if action == "help":
            print_help()
        elif action == "quit":
            print("Beenden...")
            break
        elif action == "load":

            # Check if the correct number of arguments is given
            if len(args) != 3:
                print(
                    "Ungültige Anzahl an Argumenten. Verwenden Sie 'help' um Hilfe zu erhalten.")
                continue

            file_type = args[0]
            table_name = args[1]
            file_name = args[2]

            if file_type == "excel":

                # Check if the table already exists
                if table_name in session_dataframes:
                    print(
                        f"Die Tabelle '{table_name}' existiert bereits. Überschreiben? (y/n)")
                    if input(" > ").lower() != "y":
                        continue

                # Check if the file exists
                if not os.path.exists(file_name):
                    print(f"Datei '{file_name}' existiert nicht.")
                    continue

                # Load the table
                session_dataframes[table_name] = load_table_from_excel(
                    file_name)
                print(f"Tabelle '{table_name}' erfolgreich geladen.")

            elif file_type == "csv":
                print("CSV-Dateien werden noch nicht unterstützt.")

            # Invalid file type
            else:
                print("Ungültiger Dateityp. Verwenden Sie 'help' um Hilfe zu erhalten.")

        elif action == "show":

            # Check if the correct number of arguments is given
            if len(args) < 1 or len(args) > 2:
                print(
                    "Ungültige Anzahl an Argumenten. Verwenden Sie 'help' um Hilfe zu erhalten.")
                continue

            table_name = args[0]

            # Check if the table exists
            if table_name not in session_dataframes:
                print(f"Die Tabelle '{table_name}' existiert nicht.")
                continue

            # Get the number of rows to show
            if len(args) == 2:
                try:
                    num_rows = int(args[1])
                except ValueError:
                    print("Ungültige Anzahl an Zeilen.")
                    continue
            else:
                num_rows = 5

            # Show the rows
            if num_rows == 0:
                print_table_pretty(session_dataframes[table_name])
            else:
                print_table_pretty(
                    session_dataframes[table_name].head(num_rows))

        else:
            print("Ungültige Aktion. Geben Sie 'help' ein, um Hilfe zu erhalten.")


if __name__ == "__main__":
    print("Steuernregisterabgleich")
    print("v3.0 - Juli 2024\n")
    print("Für hilfe geben Sie 'help' ein.\n")

    main_loop()
