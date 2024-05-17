import numpy as np
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import os
import time
from tkinter import messagebox
import windowMsg as miniGui

# -----------------------------------------------------------------
#           DATA TRANSFORMATION FOR  CRM FILE 
# 
# Ask the user to select a single file name.
def transform_CRM():
    increment = 0.005

    # Ask the user to select a single file name.
    miniGui.show_message_box('C.R.M')
    dir_path_file = miniGui.getFilePathGui()
    dataset = pd.read_csv(dir_path_file)
    
    #1. Trim whitespace
    dataset['Account-level fee'] = dataset['Account-level fee'].str.strip()
    dataset.rename(columns={'Account-level fee': 'account_level_fee'}, inplace=True)

    dataset['Account Number'] = dataset['Account Number'].str.strip()
    dataset.rename(columns={'Account Number': 'account_number'}, inplace=True)

    # Remove the '%' symbol and convert the column to numeric values.
    # Filter out the rows where the value is 0%.
    # Add 0.05% to the filtered values.

    # Remove '%' symbol and convert to numeric values
    dataset['account_level_fee'] = dataset['account_level_fee'].str.rstrip('%').astype(float)
    # Divide each value by 100 to convert to fraction
    dataset['account_level_fee'] = dataset['account_level_fee'] / 100

    # dataset[column] = dataset[column] + increment
    # Add the increment to non-zero percentages
    dataset.loc[dataset['account_level_fee'] != 0, 'account_level_fee'] += increment
    
    # Limit the float values to four digits of precision after the decimal point
    dataset['account_level_fee'] = dataset['account_level_fee'].apply(lambda x: f"{x:.4f}")
    
    # Save the filtered DataFrame to a new CSV file
    dataset.to_csv('filtered_CRM.csv', index=False)  


    return dataset