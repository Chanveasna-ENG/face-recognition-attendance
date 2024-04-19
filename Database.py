import os
import csv
from datetime import datetime

def create_or_check_attendance_file():
    # Define the folder name
    folder_name = "attendance"
    
    # Check if the 'attendance' folder exists, if not create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")

    # Get the current date
    current_date = datetime.now().strftime("%d-%m")
    file_name = f"{current_date}.csv"
    
    # Check if the file exists in the 'attendance' folder
    file_path = os.path.join(folder_name, file_name)
    if os.path.exists(file_path):
        print(f"The file '{file_name}' already exists in the '{folder_name}' folder.")
    else:
        # Create the CSV file with headers
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['Student ID', 'Name', 'Check-in Time', 'Check-out Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        print(f"New file '{file_name}' created in the '{folder_name}' folder.")

# Call the function to create or check the attendance file
create_or_check_attendance_file()
