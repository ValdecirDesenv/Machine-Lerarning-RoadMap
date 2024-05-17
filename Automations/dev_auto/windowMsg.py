
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import filedialog
from tkinter import messagebox



def getFilePathGui():

    application_window = tk.Tk()
    application_window.eval('tk::PlaceWindow . center')
    # Build a list of tuples for each file type the file dialog should display
    my_filetypes = [('all files', '.*'), ('text files', '.csv')]
    dir_path_file = filedialog.askopenfilename(parent=application_window,
                                    initialdir=os.getcwd(),
                                    title="Please select the T.R.D file :",
                                    filetypes=my_filetypes)
    return dir_path_file

def show_message_box(msg):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Load", f"Load {msg} file \nClick OK to continue")
    root.destroy()

# ======================================================================
#                        Delete the file generated   
# Get the current working directory
current_directory = os.getcwd()

# List of CSV files to delete
csv_files = ['filtered_CRM.csv', 'filtered_TRD.csv', 'Transition_Bonus_Upload.csv']

# Iterate through the list and delete each file
for csv_file in csv_files:
    # Construct the full path to the CSV file
    csv_file_path = os.path.join(current_directory, csv_file)
    
    # Check if the file exists
    if os.path.exists(csv_file_path):
        # Delete the file
        os.remove(csv_file_path)
        print(f"{csv_file_path} has been deleted.")
    else:
        print(f"{csv_file_path} does not exist.")

# ======================================================================
#                   PROVIDE DATE INPUT 
# Define a global variable to store the requested date
requested_Date = None
def submit_date():
    global requested_Date  # Declare requested_Date as global to use it outside this function
    date_str = date_entry.get()
    try:
        # Attempt to parse the date in the 'mm/dd/yyyy' format
        date = datetime.strptime(date_str, '%m/%d/%Y')
        requested_Date = date.strftime('%m/%d/%Y')
        # Close the window
        root.destroy()
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use MM/DD/YYYY.")

def get_date():
    global root, date_entry
    # Create the main window
    root = tk.Tk()
    root.title("Date Input")

    # Create and place the widgets
    ttk.Label(root, text="Please enter a date (DD/MM/YYYY):").grid(row=0, column=0, padx=10, pady=10)
    date_entry = ttk.Entry(root)
    date_entry.grid(row=0, column=1, padx=10, pady=10)

    submit_button = ttk.Button(root, text="Submit", command=submit_date)
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Run the application
    root.mainloop()

    # Return the requested date
    return requested_Date
# ======================================================================


if __name__ == "__main__":
    # If this file is run directly, call the get_date function
    date = get_date()
    if date:
        print(f"User entered date: {date.strftime('%m/%d/%Y')}")