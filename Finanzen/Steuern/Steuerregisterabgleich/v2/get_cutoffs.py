'''Simple script to get all entries in an excel file where the date in a column is after a cutoff date'''

import pandas
import os

# Set the cutoff date
CUTOFF_DATE = "31.12.2022"

# Set the column name
CUTOFF_DATE_FIELD = "Zuzug_Datum"

# Set the files. Every File in 'register/reg_cit_old'
files = os.listdir('register/reg_cit_old')

# Get a dataframe for every file
dfs = []
for file in files:
    dataframe = pandas.read_excel('register/reg_cit_old/' + file)
    print(f"Register file {file} read successfully")
    dfs.append(dataframe)

# Combine all dataframes
dataframe_cit = pandas.concat(dfs, ignore_index=True)

# Filter the dataframe
dataframe_cit[CUTOFF_DATE_FIELD] = pandas.to_datetime(dataframe_cit[CUTOFF_DATE_FIELD], format="%d.%m.%Y")
dataframe_cit = dataframe_cit[dataframe_cit[CUTOFF_DATE_FIELD] > pandas.to_datetime(CUTOFF_DATE, format="%d.%m.%Y")]
