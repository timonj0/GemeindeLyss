# Steuerregisterabgleich v. 1.0
# Author: Timon Jakob
# Date: 15.08.2023

#Checks if every citzen in the citizen register is in the tax register and the other way around
#If not, the missing citizens are logged in a file

# In- and output files are .excle files
# Use Pandas 

import glob
import pandas as pd
import numpy as np

# The Citizen Register consists of all the files in "register/citizen"
# The Tax Register consists of all the files in "register/tax"
# The output file containing all the citizens who are missing in either register is "register/abgleich.xlsx"

# Read all citizen files and combine them into one dataframe
citizen_files = glob.glob("register/citizen/*.xlsx") # Get all files in the folder
citizen_df = pd.DataFrame()
for file in citizen_files:
    df = pd.read_excel(file)
    citizen_df = citizen_df.append(df, ignore_index=True)

# Read all tax files and combine them into one dataframe
tax_files = glob.glob("register/tax/*.xlsx") # Get all files in the folder
tax_df = pd.DataFrame()
for file in tax_files:
    df = pd.read_excel(file)
    tax_df = tax_df.append(df, ignore_index=True)

# Check if every citizen in the citizen register is in the tax register
# If not, log the missing citizens in the output file

# Get all the citizens in the citizen register
citizen_ids = citizen_df["ID"].unique()

tax_ids = tax_df["ID"].unique() # Get all the citizens in the tax register

missing_in_tax = np.setdiff1d(citizen_ids, tax_ids) # Get all the citizens who are in the citizen register but not in the tax register
missing_in_citizen = np.setdiff1d(tax_ids, citizen_ids) # Get all the citizens who are in the tax register but not in the citizen register

# Create a dataframe with all the citizens who are missing in either register
missing_df = pd.DataFrame(columns=["ID", "missing_in_tax", "missing_in_citizen"])
missing_df["ID"] = np.concatenate((missing_in_tax, missing_in_citizen))
missing_df["missing_in_tax"] = missing_df["ID"].isin(missing_in_tax)
missing_df["missing_in_citizen"] = missing_df["ID"].isin(missing_in_citizen)

# Write the dataframe to an excel file
missing_df.to_excel("register/abgleich.xlsx", index=False)
