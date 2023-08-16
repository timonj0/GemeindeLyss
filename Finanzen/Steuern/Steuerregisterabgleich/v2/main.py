'''Steuerregisterabgleich v. 2.0'''
# Author: Timon Jakob
# Date: 08.2023

import os
import time

import pandas

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

def prepare_data_cit(dataframe):
    '''Function to prepare the data'''
    # Filter the dataframe by the cutoff date
    dataframe = filter_cutoff_date(dataframe)
    # Remove all collumns from dataframe except for the ones listed in the config file

    print("Cit Dataframe prepared successfully:")
    print(dataframe.head())

    return dataframe

if __name__ == "__main__":
    start_time = time.time()
    dataframe_cit, dataframe_tax, dataframe_qst = load_data()
    dataframe_cit = prepare_data_cit(dataframe_cit)
    dataframe_tax = prepare_data_tax(dataframe_tax, dataframe_qst)
    dataframe_missing = compare_data(dataframe_cit, dataframe_tax)
    save_data(dataframe_missing)
    runtime = time.time() - start_time
    print_statistics(dataframe_cit, dataframe_tax, dataframe_missing, runtime)
