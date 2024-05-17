import pandas as pd
import random


# Function to generate the external_id
def generate_external_id(row):
    a4 = row['start_date']
    c4 = row['rep_code']
    d4 = row['account_number']
    rand1 = format(random.randint(0, 4294967295), '08X')
    rand2 = format(random.randint(0, 65535), '04X')
    rand3 = format(random.randint(16384, 20479), '04X')
    rand4 = format(random.randint(32768, 49151), '04X')
    rand5 = format(random.randint(0, 65535), '04X')
    rand6 = format(random.randint(0, 4294967295), '08X')
    return f"{a4}-{c4}-{d4}-{rand1}-{rand2}-{rand3}-{rand4}-{rand5}{rand6}"


def generate_transition_bonus(trd_filtered, crm_filtered,dateProcess):
        # Define the header for the new DataFrame
    header = [
        'start_date', 'external_id', 'rep_code', 'account_number',
        'currency', 'client', 'asset_inflows', 'asset_outflows',
        'net_assets', 'account_level_fee'
    ]

    # Create an empty DataFrame with the specified header
    trans_bonus_up = pd.DataFrame(columns=header)
    print(trans_bonus_up.head())

    # Identify unique and repetitive account numbers
    unique_values = trd_filtered['account_number'][~trd_filtered['account_number'].duplicated(keep=False)]
    print(unique_values)

    repetitive_values = trd_filtered['account_number'][trd_filtered['account_number'].duplicated(keep=False)].unique()

    # Create a dictionary to hold DataFrames for each unique repetitive value
    repetitive_dfs = {}

    # Initialize new row template
    new_row_template = {
        'start_date': '',
        'external_id': '',
        'rep_code': '',
        'account_number': '',
        'currency': '',
        'client': '',
        'asset_inflows': 0.0,
        'asset_outflows': 0.0,
        'net_assets': 0.0,
        'account_level_fee': 0.0
    }

    # Initialize variables
    saved_AC = None
    old_value = None

    # List to hold rows to be appended
    rows_to_append = []

    # Iterate over each repetitive value
    print('# Append a new row to the DataFrame')
    for value in repetitive_values:
        if old_value != value and old_value is not None:
            # Append a new row to the list
            rows_to_append.append(new_row.copy())
        
        old_value = value

        # Filter rows with the current repetitive value
        rows_with_value = trd_filtered[trd_filtered['account_number'] == value]
        
        # Get the value in column 'account_number' of the first row of the filtered rows
        current_AC = rows_with_value.iloc[0]['account_number']
        
        # Compare the value in column 'account_number' to the saved value
        if saved_AC is None or current_AC != saved_AC:
            saved_AC = current_AC
            # Save the DataFrame in the dictionary
            repetitive_dfs[value] = rows_with_value
            
            # Update new row with values from the current row
            new_row = new_row_template.copy()
            new_row['start_date'] = dateProcess
            new_row['rep_code'] = rows_with_value.iloc[0]['rep_code']
            new_row['account_number'] = rows_with_value.iloc[0]['account_number']
            new_row['currency'] = rows_with_value.iloc[0]['currency']
            new_row['client'] = rows_with_value.iloc[0]['client']          
            if rows_with_value.iloc[0]['Net_Amount'] > 0:
                new_row['asset_inflows'] += rows_with_value.iloc[0]['Net_Amount']
            else:
                new_row['asset_outflows'] += rows_with_value.iloc[0]['Net_Amount']
            
        else:
            if rows_with_value.iloc[0]['Net_Amount'] > 0:
                new_row['asset_inflows'] += rows_with_value.iloc[0]['Net_Amount']
            else:
                new_row['asset_outflows'] += (-1 * rows_with_value.iloc[0]['Net_Amount'])
            
            # print(f"Duplicate value in column AC: '{value}':")
            # print(rows_with_value.iloc[0])

    # Append rows to the DataFrame using pd.concat
    trans_bonus_up = pd.concat([trans_bonus_up, pd.DataFrame(rows_to_append)], ignore_index=True)
    # Apply the transformation for net_assets
    trans_bonus_up['asset_outflows'] = trans_bonus_up['asset_outflows'].apply(lambda x: -x if x != 0 else x)
    trans_bonus_up['net_assets'] = trans_bonus_up['asset_inflows'] - trans_bonus_up['asset_outflows']

   
    # Merge the DataFrames on the 'account_number' column and bring in the 'account_level_fee' column from crm_filtered
    trans_bonus_up = pd.merge(trans_bonus_up, crm_filtered[['account_number', 'account_level_fee']], on='account_number', how='left')

    # Rename the 'account_level_fee_y' column to 'account_level_fee'
    trans_bonus_up = trans_bonus_up.rename(columns={'account_level_fee_y': 'account_level_fee'})

    # Drop the 'account_level_fee_x' column
    trans_bonus_up = trans_bonus_up.drop(columns=['account_level_fee_x'])

    # Apply the function to each row to create the external_id column
    trans_bonus_up['external_id'] = trans_bonus_up.apply(generate_external_id, axis=1)


    # Save the filtered DataFrame to a new CSV file
    trans_bonus_up.to_csv('Transition_Bonus_Upload.csv', index=False)
    print(trans_bonus_up)