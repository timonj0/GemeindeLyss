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
    df = pandas.read_excel(file_path)

    # Remove leading and trailing whitespaces from column names and make them lowercase
    df.columns = df.columns.str.strip().str.lower()

    return df


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
    print(" - 'find': 'find help' für Hilfe zum Befehl 'find'.")
    print(" - 'save <tabellenname>': Sichert das Resultat der letzten Abfrage in einer Tabelle.")
    print(" - 'export <tabellenname> <dateiname>': Exportiert eine Tabelle in eine Excel-Datei.")


def print_help_find():
    '''Prints the help for the find command'''
    print("Find Befehl:")
    print(" - 'find help': Zeigt diese Hilfe an.")
    print(" - 'find <tabelle_1> missing_in <tabelle_2>': Findet alle Einträge in Tabelle 1, die nicht in Tabelle 2 vorhanden sind.")
    print(" - 'find <tabelle_1> missing_in <tabelle_2> on <spalte>': Findet alle Einträge in Tabelle 1, die nicht in Tabelle 2 vorhanden sind anhand einer bestimmten Spalte. Die Spalte muss in beiden Tabellen vorhanden sein und sollte für jeden Eintrag eindeutig sein.")


def main_loop():
    '''Main loop of the program'''

    # Result of the last query
    last_query_result = pandas.DataFrame()

    while True:
        inp = input(" > ").lower().split(" ")
        action = inp[0]
        args = inp[1:]

        # Basic commands
        if action == "help":
            print_help()
        elif action == "quit":
            print("Beenden...")
            break

        # Load command
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

        # Show command
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

        # Save command
        elif action == "save":

            # Check if the correct number of arguments is given
            if len(args) != 1:
                print(
                    "Ungültige Anzahl an Argumenten. Verwenden Sie 'help' um Hilfe zu erhalten.")
                continue

            table_name = args[0]

            # Check if table doesnt already exist
            if table_name in session_dataframes:
                print(
                    f"Die Tabelle '{table_name}' existiert bereits. Überschreiben? (y/n)")
                if input(" > ").lower() != "y":
                    continue

            # Check if the last query result is empty
            if last_query_result.empty:
                print("Es gibt kein Resultat zum speichern.")
                continue

            # Save the last query result
            session_dataframes[table_name] = last_query_result
            print(f"Resultat erfolgreich als '{table_name}' gespeichert.")

        # Export command
        elif action == "export":

            # Check if the correct number of arguments is given
            if len(args) != 2:
                print(
                    "Ungültige Anzahl an Argumenten. Verwenden Sie 'help' um Hilfe zu erhalten.")
                continue

            table_name = args[0]
            file_name = args[1]

            # Check if the table exists
            if table_name not in session_dataframes:
                print(f"Die Tabelle '{table_name}' existiert nicht.")
                continue

            # Check if the file already exists
            if os.path.exists(file_name):
                print(
                    f"Die Datei '{file_name}' existiert bereits. Überschreiben? (y/n)")
                if input(" > ").lower() != "y":
                    continue

            # Export the table
            session_dataframes[table_name].to_excel(file_name, index=False)
            print(
                f"Tabelle '{table_name}' erfolgreich exportiert nach '{file_name}'.")

        # Find command
        elif action == "find":
            if len(args) == 1 and args[0] == "help":
                print_help_find()
                continue

            # missing_in subcommand
            if args[1] == "missing_in":
                # Check if the correct number of arguments is given
                if not (len(args) == 3 or len(args) == 5):
                    print(
                        "Ungültige Anzahl an Argumenten. Verwenden Sie 'help' um Hilfe zu erhalten.")
                    continue

                # missing_in base command
                if len(args) == 3:
                    # Check if the tables exist
                    if args[0] not in session_dataframes or args[2] not in session_dataframes:
                        print("Eine der Tabellen existiert nicht.")
                        continue

                    table1 = session_dataframes[args[0]]
                    table2 = session_dataframes[args[2]]

                    missing = table1[~table1.isin(table2)].dropna()
                    print_table_pretty(missing)

                # missing_in ON subcommand
                else:
                    # Check if the tables exist
                    if args[0] not in session_dataframes or args[2] not in session_dataframes:
                        print("Eine der Tabellen existiert nicht.")
                        continue

                    table1 = session_dataframes[args[0]]
                    table2 = session_dataframes[args[2]]

                    column = args[4]

                    # Check if the column exists in both tables

                    print(table1.columns)
                    print(table2.columns)
                    print(column)

                    if column not in table1.columns or column not in table2.columns:
                        print("Die Spalte existiert nicht in beiden Tabellen.")
                        continue

                    missing = table1[~table1[column].isin(table2[column])]
                    print_table_pretty(missing)

            # Invalid find subcommand
            else:
                print_help_find()

        # Invalid action
        else:
            print("Ungültige Aktion. Geben Sie 'help' ein, um Hilfe zu erhalten.")


if __name__ == "__main__":
    print("Steuernregisterabgleich")
    print("v3.0 - Juli 2024\n")
    print("Für hilfe geben Sie 'help' ein.\n")

    main_loop()
