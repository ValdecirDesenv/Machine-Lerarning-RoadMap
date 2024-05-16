import numpy as np
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import time


dir_path = os.path.dirname(os.path.realpath(__file__))
application_window = tk.Tk()
application_window.eval('tk::PlaceWindow . center')
# Build a list of tuples for each file type the file dialog should display
my_filetypes = [('all files', '.*'), ('text files', '.csv')]

# -----------------------------------------------------------------
#           DATA TRANSFORMATION FOR  TRD FILE 
# 

def transform_TRD():

        # Ask the user to select a single file name.
    dir_path_file = filedialog.askopenfilename(parent=application_window,
                                        initialdir=os.getcwd(),
                                        title="Please select the T.R.D file :",
                                        filetypes=my_filetypes)
    
    dataset = pd.read_csv(dir_path_file, usecols=[0,1,6,9,12]) # Columns A,B,G,J,R
    #1. Trim whitespace
    dataset['Security Symbol'] = dataset['Security Symbol'].str.strip()
    dataset.rename(columns={'Security Symbol': 'Security_Symbol'}, inplace=True)

    #  Our_symbols
    # Define the array of values to filter
    values_to_keep = ['BAM.A', 'BCE', 'BMO', 'CM', 'ENB', 'MFC', 'POW', 'RY', 'TD', 'XIU',
            'AAPL', 'AMZN', 'BRK.B', 'COST', 'DIA', 'GOOG', 'JPM', 'META', 'MSFT',
            'V', 'WFC', 'WMT', 'XCB', 'XRE', 'USRT', 'HDV', 'USIG',
            'TDB407', 'TDB451', 'BAM', 'BN', 'IUSG','OPO']

    # Construct the query string dynamically
    # Define the condition to filter the DataFrame
    query_string = "Security_Symbol.str.startswith('opt') | Security_Symbol in @values_to_keep"

    # Filter the DataFrame using the query() method
    df_filtered = dataset.query(query_string)

    
    # Rewrite TRADE TYPE COLUMN WITH :
    # AB ABT BP as BUY
    # AS AST SP as SELL
    # OTHERS ... keep ? ? ?

    dataset.replace('AB', 'BUY', inplace=True)
    dataset.replace('ABT','BUY', inplace=True)
    dataset.replace('BP', 'BUY', inplace=True)
    dataset.replace('AS', 'SELL', inplace=True)
    dataset.replace('SP', 'SELL', inplace=True)
    
    # Save the filtered DataFrame to a new CSV file
    df_filtered.to_csv('filtered_TRD.csv', index=False)


    return df_filtered

# -----------------------------------------------------------------
#           DATA TRANSFORMATION FOR  CRM FILE 
# 
# Ask the user to select a single file name.
def transform_CRM():
    increment = 0.005
    show_message_box('C R M')
    dir_path_file = filedialog.askopenfilename(parent=application_window,
                                        initialdir=os.getcwd(),
                                        title="Please select the CPM-ACCOUNTS  file :",
                                        filetypes=my_filetypes)

    dataset = pd.read_csv(dir_path_file)
    
    #1. Trim whitespace
    dataset['Account-level fee'] = dataset['Account-level fee'].str.strip()
    dataset.rename(columns={'Account-level fee': 'Account_level_fee'}, inplace=True)

    # Remove the '%' symbol and convert the column to numeric values.
    # Filter out the rows where the value is 0%.
    # Add 0.05% to the filtered values.
    column = 'Account_level_fee'
    # Remove '%' symbol and convert to numeric values
    dataset[column] = dataset[column].str.rstrip('%').astype(float)
    # Divide each value by 100 to convert to fraction
    dataset[column] = dataset[column] / 100

    # dataset[column] = dataset[column] + increment
    # Add the increment to non-zero percentages
    dataset.loc[dataset[column] != 0, column] += increment
    
    # Limit the float values to four digits of precision after the decimal point
    dataset[column] = dataset[column].apply(lambda x: f"{x:.4f}")
    
    # Save the filtered DataFrame to a new CSV file
    dataset.to_csv('filtered_CRM.csv', index=False)

    # Extract the header (column names)
    header = dataset.columns.tolist()


    # Create an empty DataFrame with the specified header
    dataset = pd.DataFrame(columns=header)

    # Save the empty DataFrame to a CSV file
    dataset.to_csv('tests.csv', index=False)

    # Print the header
    print(header)


    return dataset

def show_message_box(msg):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Load", f"Load {msg} file \nClick OK to continue")
    root.destroy()


def main():
    print(' Let us do')
    # print(transform_TRD())
    # time.sleep(3)
    print(transform_CRM())
    




# Check if this script is being run directly as the main module
if __name__ == "__main__":
    main()