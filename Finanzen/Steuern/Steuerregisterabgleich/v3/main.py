'''Steuerregisterabgleich v3.0'''
# Version 3.0: Interactive CLI tool
# Author: Timon Jakob
# Date: 07.2023

import os
import sys
import pandas

# HashMap to store the dataframes with the corresponding name
session_dataframes = {}


def load_table_from_excel(file_path: str) -> pandas.DataFrame:
    '''Load a table from an Excel file'''
    df = pandas.read_excel(file_path)

    # Remove leading and trailing whitespaces from column names and make them lowercase
    df.columns = df.columns.str.strip().str.lower()

    return df


def load_on_start(args: list):
    '''Load tables on start'''
    for i in range(1, len(args), 2):
        file_name = args[i]
        table_name = args[i+1]

        if not os.path.exists(file_name):
            print(f"Datei '{file_name}' existiert nicht.")
            continue

        session_dataframes[table_name] = load_table_from_excel(file_name)
        print(f"Tabelle '{table_name}' erfolgreich geladen.")


def filter_by_date(df: pandas.DataFrame, column: str, filter_by: str, date: str) -> pandas.DataFrame:
    '''filter a table by a date. The date must be in the format DD.MM.YYYY. Can filter_by by before, after or on equal'''
    date = pandas.to_datetime(date, format="%d.%m.%Y")
    if filter_by == "before":
        return df[pandas.to_datetime(df[column], format="%d.%m.%Y") < pandas.to_datetime(date, format="%d.%m.%Y")]
    elif filter_by == "after":
        return df[pandas.to_datetime(df[column], format="%d.%m.%Y") > pandas.to_datetime(date, format="%d.%m.%Y")]
    elif filter_by == "on":
        return df[pandas.to_datetime(df[column], format="%d.%m.%Y") == pandas.to_datetime(date, format="%d.%m.%Y")]
    else:
        print("Ungültiger Filter. Verwenden Sie 'before', 'after' oder 'on'.")
        return df


def combine_tables(df1: pandas.DataFrame, df2: pandas.DataFrame):
    '''Combine two dataframes'''
    return pandas.concat([df1, df2])

def rename_column(df: pandas.DataFrame, old_name: str, new_name: str) -> pandas.DataFrame:
    '''Rename a column in a dataframe'''
    df.rename(columns={old_name: new_name}, inplace=True)
    return df

def find_in_table(df1: pandas.DataFrame, df2: pandas.DataFrame) -> pandas.DataFrame:
    '''Find all entries in df1 that are also in df2'''
    return df1[df1.isin(df2).all(1)]

def find_in_table_on_column(df1: pandas.DataFrame, df2: pandas.DataFrame, column: str) -> pandas.DataFrame:
    '''Find all entries in df1 that are also in df2 based on a column'''
    return df1[df1[column].isin(df2[column])]
 

def print_table_pretty(table: pandas.DataFrame, total_rows: int):
    '''Prints a table in a pretty format'''
    print(f"Zeilen: {total_rows}")
    print(table.to_string(index=False))


def print_help():
    '''Prints the help'''
    print("Hilfe:")
    print(" - 'help': Zeigt diese Hilfe an")
    print(" - 'quit': Beendet das Programm")
    print(" - 'load <excel/csv> <tabellenname> <dateiname>': Lädt eine Tabelle aus einer Excel- oder CSV-Datei.")
    print(" - 'show <tabellenname> <(anzahl)>': Zeigt die ersten n Zeilen der Tabelle an. Standardmäßig 5 Zeilen. 0 zeigt alle Zeilen an.")
    print(" - 'save <tabellenname>': Sichert das Resultat der letzten Abfrage in einer Tabelle.")
    print(" - 'export <tabellenname> <dateiname>': Exportiert eine Tabelle in eine Excel-Datei.")
    print(" - 'rename <tabellenname> <spalte_alt> <spalte_neu>': Benennt eine Spalte in einer Tabelle um.")
    print(" - 'combine <tabellenname_1> <tabellenname_2> <tabellenname_neu>': Kombiniert zwei Tabellen und speichert das Resultat in einer neuen Tabelle.")
    print(" - 'find': 'find help' für Hilfe zum Befehl 'find'.")
    print(" - 'filter_by_date <tabellenname> <spalte> <'before'/'after'/'on'> <datum>': Filtert eine Tabelle nach einem Datum. Das Datum muss im Format DD.MM.YYYY sein.")


def print_help_find():
    '''Prints the help for the find command'''
    print("Find Befehl:")
    print(" - 'find help': Zeigt diese Hilfe an.")
    print(" - 'find <tabelle_1> in <tabelle_2>': Findet alle Einträge in Tabelle 1, die auch in Tabelle 2 vorhanden sind.")
    print(" - 'find <tabelle_1> in <tabelle_2>' on <spaltenname>: Findet alle Einträge in Tabelle 1, die auch in Tabelle 2 vorhanden sind anhand einer Spalte. Die Spalte muss in beiden Tabellen vorhanden sein")
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
                print_table_pretty(session_dataframes[table_name], session_dataframes[table_name].shape[0])
            else:
                print_table_pretty(
                    session_dataframes[table_name].head(num_rows), session_dataframes[table_name].shape[0])

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
                    last_query_result = missing
                    print_table_pretty(missing, missing.shape[0])

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
                    last_query_result = missing
                    print_table_pretty(missing, missing.shape[0])

            # find in subcommand
            elif args[1] == "in":
                # Check if the correct number of arguments is given
                if not (len(args) == 3 or len(args) == 5):
                    print(
                        "Ungültige Anzahl an Argumenten. Verwenden Sie 'help' um Hilfe zu erhalten.")
                    continue

                # find in base command
                if len(args) == 3:
                    # Check if the tables exist
                    if args[0] not in session_dataframes or args[2] not in session_dataframes:
                        print("Eine der Tabellen existiert nicht.")
                        continue

                    table1 = session_dataframes[args[0]]
                    table2 = session_dataframes[args[2]]

                    found = find_in_table(table1, table2)
                    last_query_result = found
                    print_table_pretty(found, found.shape[0])

                # find in ON subcommand
                else:
                    # Check if the tables exist
                    if args[0] not in session_dataframes or args[2] not in session_dataframes:
                        print("Eine der Tabellen existiert nicht.")
                        continue

                    table1 = session_dataframes[args[0]]
                    table2 = session_dataframes[args[2]]

                    column = args[4]

                    # Check if the column exists in both tables
                    if column not in table1.columns or column not in table2.columns:
                        print("Die Spalte existiert nicht in beiden Tabellen.")
                        continue

                    found = find_in_table_on_column(table1, table2, column)
                    last_query_result = found
                    print_table_pretty(found, found.shape[0])

            # Invalid find subcommand
            else:
                print_help_find()

        # Filter by date command
        elif action == "filter_by_date":

            # Check if the correct number of arguments is given
            if len(args) != 4:
                print(
                    "Ungültige Anzahl an Argumenten. Verwenden Sie 'help' um Hilfe zu erhalten.")
                continue

            table_name = args[0]
            column = args[1]
            filter_by = args[2]
            date = args[3]

            # Check if the table exists
            if table_name not in session_dataframes:
                print(f"Die Tabelle '{table_name}' existiert nicht.")
                continue

            # Check if the column exists
            if column not in session_dataframes[table_name].columns:
                print(
                    f"Die Spalte '{column}' existiert nicht in der Tabelle '{table_name}'.")
                continue

            # Filter the table
            filtered_table = filter_by_date(
                session_dataframes[table_name], column, filter_by, date)
            last_query_result = filtered_table
            print_table_pretty(filtered_table, filtered_table.shape[0])


        # Combine command
        elif action == "combine":

            # Check if the correct number of arguments is given
            if len(args) != 3:
                print(
                    "Ungültige Anzahl an Argumenten. Verwenden Sie 'help' um Hilfe zu erhalten.")
                continue

            table1_name = args[0]
            table2_name = args[1]
            new_table_name = args[2]

            # Check if the tables exist
            if table1_name not in session_dataframes or table2_name not in session_dataframes:
                print("Eine der Tabellen existiert nicht.")
                continue

            # Combine the tables
            combined_table = combine_tables(
                session_dataframes[table1_name], session_dataframes[table2_name])
            session_dataframes[new_table_name] = combined_table
            print(
                f"Tabellen '{table1_name}' und '{table2_name}' erfolgreich kombiniert und als '{new_table_name}' gespeichert.")


        # Rename command
        elif action == "rename":
                
                # Check if the correct number of arguments is given
                if len(args) != 3:
                    print(
                        "Ungültige Anzahl an Argumenten. Verwenden Sie 'help' um Hilfe zu erhalten.")
                    continue
    
                table_name = args[0]
                old_name = args[1]
                new_name = args[2]
    
                # Check if the table exists
                if table_name not in session_dataframes:
                    print(f"Die Tabelle '{table_name}' existiert nicht.")
                    continue
    
                # Check if the column exists
                if old_name not in session_dataframes[table_name].columns:
                    print(
                        f"Die Spalte '{old_name}' existiert nicht in der Tabelle '{table_name}'.")
                    continue
    
                # Rename the column
                renamed_table = rename_column(
                    session_dataframes[table_name], old_name, new_name)
                session_dataframes[table_name] = renamed_table
                print(
                    f"Spalte '{old_name}' in Tabelle '{table_name}' erfolgreich in '{new_name}' umbenannt.")


        # Invalid action
        else:
            print("Ungültige Aktion. Geben Sie 'help' ein, um Hilfe zu erhalten.")


if __name__ == "__main__":
    print("Steuernregisterabgleich")
    print("v3.0 - Juli 2024\n")
    print("Für hilfe geben Sie 'help' ein.\n")

    args = sys.argv[1:]
    if len(args) > 0 and args[0] == "-load":
        load_on_start(args)

    main_loop()
