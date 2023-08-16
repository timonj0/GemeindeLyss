'''Steuerregisterabgleich v. 2.0'''
# Author: Timon Jakob
# Date: 08.2023

import os
import time

import pandas
import configparser

CUTOFF_DATE = "01.01.1900"
CUTOFF_DATE_FIELD = "Zuzug_Datum"
DATA_CIT_FORMAT = []

AHV_FIELD = "AHV-VN"

def load_data():
    '''Function to load the data'''

    # Get all files for the citizen register
    print(f"Reading citizen register files: {os.listdir('register/reg_cit')}")
    files = os.listdir('register/reg_cit')

    # Get a dataframe for every file
    dfs = []
    for file in files:
        dataframe = pandas.read_excel('register/reg_cit/' + file)
        print(f"Register file {file} read successfully")
        dfs.append(dataframe)

    # Combine all dataframes
    dataframe_cit = pandas.concat(dfs, ignore_index=True)

    # Get all files for the tax register
    print(f"Reading tax register files: {os.listdir('register/reg_tax')}")
    files = os.listdir('register/reg_tax')

    # Get a dataframe for every file
    dfs = []
    for file in files:
        dataframe = pandas.read_excel('register/reg_tax/' + file)
        print(f"Register file {file} read successfully")
        dfs.append(dataframe)

    # Combine all dataframes
    dataframe_tax = pandas.concat(dfs, ignore_index=True)

    # Get all files for the qst register
    print(f"Reading qst register files: {os.listdir('register/reg_qst')}")
    files = os.listdir('register/reg_qst')

    # Get a dataframe for every file
    dfs = []
    for file in files:
        dataframe = pandas.read_excel('register/reg_qst/' + file)
        print(f"Register file {file} read successfully")
        dfs.append(dataframe)

    # Combine all dataframes
    dataframe_qst = pandas.concat(dfs, ignore_index=True)

    return dataframe_cit, dataframe_tax, dataframe_qst

def filter_cutoff_date(dataframe):
    '''Function to filter the dataframe by the cutoff date'''
    dataframe[CUTOFF_DATE_FIELD] = pandas.to_datetime(dataframe[CUTOFF_DATE_FIELD], format="%d.%m.%Y")
    dataframe = dataframe[dataframe[CUTOFF_DATE_FIELD] <= pandas.to_datetime(CUTOFF_DATE, format="%d.%m.%Y")]
    return dataframe


def prepare_data_cit(dataframe):
    '''Function to prepare the data'''
    # Filter the dataframe by the cutoff date
    dataframe = filter_cutoff_date(dataframe)
    # Remove all collumns from dataframe except for the ones listed in the config file

    print("CIT Dataframe prepared successfully:")
    print(dataframe.head())

    return dataframe

def prepare_data_tax(dataframe_tax, dataframe_qst):
    '''Function to prepare the data'''
    # Preparing tax data got easy in v2. Only a dataframe with all the AHV-Codes of the entire tax register is needed.
    dataframe_tax = dataframe_tax[[AHV_FIELD]]
    dataframe_qst = dataframe_qst[[AHV_FIELD]]

    # Combine all dataframes
    dataframe_tax = pandas.concat([dataframe_tax, dataframe_qst], ignore_index=True)

    # Remove all duplicates
    dataframe_tax = dataframe_tax.drop_duplicates()

    print("TAX Dataframe prepared successfully:")
    print(dataframe_tax.head())

    return dataframe_tax

def compare_data(dataframe_cit, dataframe_tax):
    '''Function to compare the data'''
    # Compare the dataframes
    dataframe_missing = pandas.merge(dataframe_cit, dataframe_tax, on=AHV_FIELD, how='left', indicator=True)
    dataframe_missing = dataframe_missing[dataframe_missing['_merge'] == 'left_only']
    dataframe_missing = dataframe_missing.drop(columns=['_merge'])

    print("Comparison of dataframes successful.")
    print(dataframe_missing.head())

    return dataframe_missing

if __name__ == "__main__":
    # Configuration
    config = configparser.ConfigParser()
    config.read('config.cfg')
    CUTOFF_DATE = config['DATA']['CUTOFF_DATE']
    CUTOFF_DATE_FIELD = config['DATA']['CUTOFF_DATE_FIELD']
    DATA_CIT_FORMAT = config['DATA']['DATA_CIT_FORMAT']

    AHV_FIELD = config['DATA']['AHV-FIELD']

    start_time = time.time()
    dataframe_cit, dataframe_tax, dataframe_qst = load_data()
    dataframe_cit = prepare_data_cit(dataframe_cit)
    dataframe_tax = prepare_data_tax(dataframe_tax, dataframe_qst)
    dataframe_missing = compare_data(dataframe_cit, dataframe_tax)
    save_data(dataframe_missing)
    runtime = time.time() - start_time
    print_statistics(dataframe_cit, dataframe_tax, dataframe_missing, runtime)
