import pandas as pd
import windowMsg as miniGui


# -----------------------------------------------------------------
#           DATA TRANSFORMATION FOR  TRD FILE 
# 

def transform_TRD():

    # Ask the user to select a single file name.
    miniGui.show_message_box('T.R.D')
    dir_path_file = miniGui.getFilePathGui()
    dataset = pd.read_csv(dir_path_file, usecols=[0,1,3,5,6,9,12,14]) # Columns A,B,F,G,J,R,O
    #1. Trim whitespace  account_number
    #dataset['Account Name'] = dataset['Account Name'].str.strip()
    dataset.rename(columns={'Account Name': 'client'}, inplace=True)

    dataset['Account Number'] = dataset['Account Number'].str.strip()
    dataset.rename(columns={'Account Number': 'account_number'}, inplace=True)

    dataset['Account Currency'] = dataset['Account Currency'].str.strip()
    dataset.rename(columns={'Account Currency': 'currency'}, inplace=True)

    dataset['Security Symbol'] = dataset['Security Symbol'].str.strip()
    dataset.rename(columns={'Security Symbol': 'Security_Symbol'}, inplace=True)
    
    dataset['Account RR Code'] = dataset['Account RR Code'].str.strip()
    dataset.rename(columns={'Account RR Code': 'rep_code'}, inplace=True)
    
    # dataset['Net Amount'] = dataset['Net Amount'].str.strip()
    dataset.rename(columns={'Net Amount': 'Net_Amount'}, inplace=True)
    
    # dataset['Trade Type'] = dataset['Trade Type'].str.strip()
    dataset.rename(columns={'Trade Type': 'Trade_Type'}, inplace=True)
    
    # Column[G] name : < Trade Type > 
    #          ----    Rewrite TRADE TYPE COLUMN WITH -----  
    # AB ABT BP as BUY
    # AS AST SP as SELL
    # OTHERS ... keep ? ? ?
    dataset.replace('AB', 'BUY', inplace=True)
    dataset.replace('ABT','BUY', inplace=True)
    dataset.replace('BP', 'BUY', inplace=True)
    dataset.replace('AS', 'SELL', inplace=True)
    dataset.replace('SP', 'SELL', inplace=True)
    
    
    # Column[J] name : < Security Symbol >   
    #                        ---     Our_symbols    -----
    # Define the array of values to filter
    # It will remove all rows that does not match this condition
    Our_symbols_to_keep = ['BAM.A', 'BCE', 'BMO', 'CM', 'ENB', 'MFC', 'POW', 'RY', 'TD', 'XIU',
            'AAPL', 'AMZN', 'BRK.B', 'COST', 'DIA', 'GOOG', 'JPM', 'META', 'MSFT',
            'V', 'WFC', 'WMT', 'XCB', 'XRE', 'USRT', 'HDV', 'USIG',
            'TDB407', 'TDB451', 'BAM', 'BN', 'IUSG','OPO']
    # Construct the query string dynamically
    # Define the condition to filter the DataFrame
    query_string = "Security_Symbol.str.startswith('opt') | Security_Symbol in @Our_symbols_to_keep"
    # Filter the DataFrame using the query() method
    df_filtered = dataset.query(query_string)


    # Column[B] name : < Account RR Code >   
    #                        ---     Our_symbols    -----
    # Define the array of values to filter
    # It will remove all rows that does not match this condition
    security_symbol_to_keep = [
    'A5FS', 'A5FP', 'A7EE', 'A7F6', 'A5FT',
    'A5FU', 'A5FR', 'A5BD', 'A5FQ', 'A7FF',
    'A7FN', 'A5Y2', 'A7FM', 'A5Y1', 'A5Y4',
    'A5Y6', 'A7ED', 'A5Y8', 'A7EC', 'A7GC',
    'A7EB', 'A7GB', 'A7EH', 'A7EI', 'A7EA',
    'A5CM', 'A7EF', 'A7GA', 'A7GP', 'A5Y0',
    'A7GJ', 'A7GL', 'A7GM', 'A5Y5', 'A7EG',
    'A7GT', 'A7GS', 'A7GR', 'A7GO', 'A5B1',
    'A7EJ', 'A5B3', 'A5B0', 'A5B4', 'A5B2',
    'A7GQ', 'A7GH', 'A7GN', 'A5B8', 'A5B6',
    'A5B5', 'A5BI', 'A5BO', 'A5BN', 'A5BG',
    'A5BM', 'A5BB', 'A5BF', 'A5BK', 'A5BH',
    'A5B9', 'A5G6', 'A5BX', 'A5BA', 'A5BL',
    'A5BV', 'A5BW', 'A5BU', 'A5BZ', 'A5BS',
    'A5BT', 'A5CN', 'A5CL', 'A5CO', 'A5CR',
    'A5CP', 'A7FS', 'A7FQ', 'A7FR', 'A7FY',
    'A7FX', 'A5JK', 'A5JI', 'A7FW', 'A5JM',
    'A5JJ', 'A5JL', 'A5JN', 'A5JX', 'A5JH',
    'A5JO', 'A5JS', 'A5JQ', 'A7GY', 'A7GW',
    'A7GZ', 'A5JW', 'A5JG', 'A7GV', 'A5JT',
    'A5JV', 'A5JU', 'A7GX', 'A5JZ', 'A7GU',
    'A7HD'
    ]

    query_string = "rep_code in @security_symbol_to_keep"
    # Filter the DataFrame using the query() method
    df_filtered = dataset.query(query_string)

    # Column[O] name : < Trade Type >  
    # Function to change the sign of the value if action is 'SELL'
    # As the value is already numeric, just keep and continue         
    # Ensure 'Net_Amount' is numeric
    df_filtered['Net_Amount'] = pd.to_numeric(df_filtered['Net_Amount'], errors='coerce')
    # print(df_filtered.head())
    df_filtered['Net_Amount'] = df_filtered.apply(lambda row: (row['Net_Amount'] - 0) if row['Trade_Type'] == 'SELL' else row['Net_Amount'], axis=1)

    # print("DataFrame after changing 'Net_Amount' values for 'SELL' actions:")
    # print(df_filtered.head())
#     print(df_filtered.head())
    
    # Save the filtered DataFrame to a new CSV file
    df_filtered.to_csv('filtered_TRD.csv', index=False)
#     print(df_filtered.head())
    
    return df_filtered

