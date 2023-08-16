'''Steuerregisterabgleich v. 1.1'''
# Author: Timon Jakob
# Date: 08.2023

import datetime
import configparser
import os
import pandas
pandas.options.mode.chained_assignment = None  # default='warn'

CHECK_QST = True
CUTOFF_DATE = "01.01.1900"


def filter_cutoff_date(dataframe):
    '''Function to filter the dataframe by the cutoff date'''
    dataframe["Zuzug_Datum"] = pandas.to_datetime(dataframe["Zuzug_Datum"], format="%d.%m.%Y")
    dataframe = dataframe[dataframe["Zuzug_Datum"] <= pandas.to_datetime(CUTOFF_DATE, format="%d.%m.%Y")]
    return dataframe

# Function to compare two dataframes and find missing rows
def find_missing_rows(df1, df2):
    '''Function to compare two dataframes and find missing rows'''
    missing_rows = df1.merge(df2, how='left', indicator=True)
    missing_rows = missing_rows[missing_rows['_merge'] == 'left_only']
    missing_rows = missing_rows.drop('_merge', axis=1)
    return missing_rows

# Function to prepare the data
def prepare_data_cit(dataframe):
    '''Function to prepare the data'''
    # Filter the dataframe by the cutoff date
    dataframe = filter_cutoff_date(dataframe)
    # Remove all collumns from dataframe except for the ones listed below
    data_points = ["NameEinwohner", "Rufname", "Geburtsdatum", "AdresszusatzStrasseHausStrassenzusatz", "PLZOrt", "Zivilstand"]
    dataframe = dataframe[data_points]
    # Split the column "PLZOrt" into two columns "PLZ" and "Ort" by splitting the string at the first space.
    dataframe["PLZOrt"].fillna("", inplace=True)  # Replace NaN with empty string
    dataframe[["PLZ", "Ort"]] = dataframe["PLZOrt"].str.split(pat=" ", n=1, expand=True)
    # Remove the column "PLZOrt"
    dataframe = dataframe.drop("PLZOrt", axis=1)
    # Make the column "Geburtsdatum" a datetime object
    dataframe["Geburtsdatum"] = pandas.to_datetime(dataframe["Geburtsdatum"], format="%d.%m.%Y")
    # Make the PLZ a string
    dataframe["PLZ"].fillna(1, inplace=True)  # Replace NaN with 1
    dataframe["PLZ"] = dataframe["PLZ"].astype(int).astype(str)
    # Make letters in the dataframe uppercase
    dataframe = dataframe.apply(lambda x: x.str.upper() if x.dtype == "object" else x)
    # Sort the columns in the dataframe
    dataframe = dataframe[["NameEinwohner", "Rufname", "Geburtsdatum", "AdresszusatzStrasseHausStrassenzusatz", "PLZ", "Ort", "Zivilstand"]]
    # Rename the columns
    dataframe = dataframe.rename(columns={"NameEinwohner": "Name", "Rufname": "Vorname", "AdresszusatzStrasseHausStrassenzusatz": "Strasse"})

    print("Cit Dataframe prepared successfully:")
    print(dataframe.head())

    return dataframe

def prepare_data_tax(dataframe):
    '''Function to prepare the data'''
    # Remove all collumns from dataframe except for the ones listed below
    data_points = ["Name", "Vornamen", "Geburtsdatum", "Strasse", "PLZ", "Ort", "Zivilstand"]
    dataframe = dataframe[data_points]
    # Remove middle names from the column "Vornamen" by splitting the string at the first space.
    dataframe["Vornamen"].fillna("", inplace=True)  # Replace NaN with empty string
    dataframe[["Vorname", "Mittelname"]] = dataframe["Vornamen"].str.split(pat=" ", n=1, expand=True)
    # Make PLZ a string without decimal places
    dataframe["PLZ"].fillna(1, inplace=True)  # Replace NaN with 1
    dataframe["PLZ"] = dataframe["PLZ"].astype(int).astype(str)
    # Remove the column "Vornamen"
    dataframe = dataframe.drop("Mittelname", axis=1)
    # Make the column "Geburtsdatum" a datetime object
    dataframe["Geburtsdatum"] = pandas.to_datetime(dataframe["Geburtsdatum"], format="%d.%m.%Y")
    # Remove all "BE" suffixes from the column "Ort" and remove the last space
    dataframe["Ort"] = dataframe["Ort"].str.replace("BE", "")
    dataframe["Ort"] = dataframe["Ort"].str.rstrip()
    # Make letters in the dataframe uppercase
    dataframe = dataframe.apply(lambda x: x.str.upper() if x.dtype == "object" else x)
    # Sort the columns in the dataframe
    dataframe = dataframe[["Name", "Vorname", "Geburtsdatum", "Strasse", "PLZ", "Ort", "Zivilstand"]]

    print("Tax Dataframe prepared successfully:")
    print(dataframe.head())

    return dataframe

def prepare_data_qst(dataframe):
    '''Function to prepare the data'''
    # Remove all collumns from dataframe except for the ones listed below
    data_points = ["Name", "Vorname"]
    dataframe = dataframe[data_points]
    # Remove middle names from the column "Vornamen" by splitting the string at the first space.
    dataframe["Vorname"].fillna("", inplace=True)  # Replace NaN with empty string
    dataframe[["Vorname", "Mittelname"]] = dataframe["Vorname"].str.split(pat=" ", n=1, expand=True)
    # Remove the column "Mittelname"
    dataframe = dataframe.drop("Mittelname", axis=1)
    # Make letters in the dataframe uppercase
    dataframe = dataframe.apply(lambda x: x.str.upper() if x.dtype == "object" else x)


    print("Qst Dataframe prepared successfully:")
    print(dataframe.head())

    return dataframe


def load_data():
    '''Function to load the data'''

    # Get every file in 'register/reg_citizen'
    print(f"Reading citizen register files: {os.listdir('register/reg_citizen')}")
    files = os.listdir('register/reg_citizen')

    # Get a dataframe for every file
    dfs = []
    for file in files:
        print(f"Reading register file: {file}")
        df = pandas.read_excel('register/reg_citizen/' + file)
        print(f"Register file {file} read successfully")
        dfs.append(df)

    # Combine all dataframes
    df_cit = pandas.concat(dfs, ignore_index=True)

    # Get every file in 'register/reg_tax'
    print(f"Reading tax register files: {os.listdir('register/reg_tax')}")
    files = os.listdir('register/reg_tax')

    # Get a dataframe for every file
    dfs = []
    for file in files:
        print(f"Reading register file: {file}")
        df = pandas.read_excel('register/reg_tax/' + file)
        print(f"Register file {file} read successfully")
        dfs.append(df)

    # Combine all dataframes
    df_tax = pandas.concat(dfs, ignore_index=True)

    # Get every file in 'register/reg_qst'
    print(f"Reading qst register files: {os.listdir('register/reg_qst')}")
    files = os.listdir('register/reg_qst')

    # Get a dataframe for every file
    dfs = []
    for file in files:
        print(f"Reading register file: {file}")
        df = pandas.read_excel('register/reg_qst/' + file)
        print(f"Register file {file} read successfully")
        dfs.append(df)

    # Combine all dataframes
    df_qst = pandas.concat(dfs, ignore_index=True)

    # Prepare the data
    df_cit = prepare_data_cit(df_cit)
    df_tax = prepare_data_tax(df_tax)
    df_qst = prepare_data_qst(df_qst)

    return df_cit, df_tax, df_qst


def check(df_cit, df_tax, df_qst):
    '''Function to check if all citizens are in the tax register'''
    # Check if all citizens in df_cit are in df_tax. If not, add citizen to a new dataframe with the same columns as df_cit.
    # Use pandas merge to check if a citizen is in df_tax.

    print("Checking if all citizens are in tax register...")
    df_missing = find_missing_rows(df_cit, df_tax)
    # Remove duplicates based on all columns
    df_missing = df_missing.drop_duplicates()

    if CHECK_QST:
        print(f"Missing before checking qst: {len(df_missing)}")
        # Merge the dataframes on "Name" and "Vorname"
        merged_df = df_missing.merge(df_qst, on=["Name", "Vorname"], how="left", indicator=True)
        filtered_df = merged_df[merged_df["_merge"] == "left_only"]
        filtered_df = filtered_df[df_missing.columns]
        df_missing = filtered_df
        print(f"Missing after checking qst: {len(df_missing)}")

    print(f"Dataframe of missing citizens with {len(df_missing)} entries prepared successfully:")
    print(df_missing.head())

    return df_missing


def display(df_cit, df_tax, df_qst, df_missing):
    '''Function to display and output the data'''
    # Print statistics
    print("\n\n")
    print("Statistics:")
    print(f"Number of citizens in citizen register:              {len(df_cit)}")
    print(f"Number of citizens in tax register:                  {len(df_tax)}")
    print(f"Number of citizens in qst register:                  {len(df_qst)}")
    print(f"Number of citizens that are not in the tax register: {len(df_missing)}")


    # Output the new dataframe as an excel file namend "output_%d_%m_%y.xlsx"
    df_missing.to_excel("output_" + datetime.datetime.now().strftime("%d_%m_%y") + ".xlsx", index=False)
    print(f"Output file 'register/output_{datetime.datetime.now().strftime('%d_%m_%y')}.xlsx' created successfully")

if __name__ == "__main__":
    # Configure script
    config = configparser.ConfigParser()
    config.read("config.cfg")
    CHECK_QST = config.getboolean("CONFIG", "CHECK_QST")
    CUTOFF_DATE = config.get("CONFIG", "CUTOFF_DATE")
    
    # Load the data
    df_cit, df_tax, df_qst = load_data()

    # Check if all citizens are in the tax register
    df_missing = check(df_cit, df_tax, df_qst)

    # Display and output the data
    display(df_cit, df_tax, df_qst, df_missing)
