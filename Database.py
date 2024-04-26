import os
import csv
from datetime import datetime, timedelta


# Define the folder name
FOLDER_NAME = "attendance"
file_name = f"{datetime.now().strftime('%d-%m')}.csv"
file_path = os.path.join(FOLDER_NAME, file_name)


def write_to_csv(rows=None, row=None, write_header=False):
    csvfile = open(file_path, 'w' if write_header else 'a', newline='')
    fieldnames = ['Student ID', 'Name', 'Check-in Time', 'Check-out Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    if write_header and rows != None:
        writer.writeheader()
        writer.writerows(rows)
    elif write_header:
        writer.writeheader()
    elif row != None:
        writer.writerow(row)

    csvfile.close()


def create_or_check_attendance_file():
    # Check if the 'attendance' folder exists, if not create it
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
        print(f"Folder '{FOLDER_NAME}' created.")

    if not os.path.exists(file_path):
        write_to_csv(write_header=True)
        print(f"New file '{file_name}' created in the '{FOLDER_NAME}' folder.")


def mark_attendance(name, student_id):
    # Load the CSV file content into a list of dictionaries
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    checked_out = False
    already_checked_in = False
    current_time = datetime.now()
    current_time_str = current_time.strftime("%H:%M:%S")

    # Iterate over the rows
    for row in rows:
        if row['Name'] != name:
            continue

        already_checked_in = True

        if row['Check-out Time'] != '':
            continue

        check_in_time = datetime.strptime(row['Check-in Time'], "%H:%M:%S")
        check_in_time = check_in_time.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        
        if current_time - check_in_time >= timedelta(hours=1):
            row['Check-out Time'] = current_time_str
            checked_out = True
        
    # Write the updated rows back to the CSV file
    if checked_out:
        write_to_csv(rows=rows, row=None, write_header=True)
    elif not already_checked_in:
        row = {'Student ID': student_id, 'Name': name, 'Check-in Time': current_time_str, 'Check-out Time': ''}
        write_to_csv(rows=None, row=row, write_header=False)
