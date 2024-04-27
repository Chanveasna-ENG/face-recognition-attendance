import os
import csv
from datetime import datetime, timedelta


script_dir = os.path.dirname(os.path.realpath(__file__))

# Define the folder name
FOLDER_NAME = "attendance"
file_name = f"{datetime.now().strftime('%d-%m')}.csv"

file_path = os.path.join(script_dir, FOLDER_NAME, file_name)


CHECK_IN_DELAY = 30 # second
CHECK_OUT_DELAY = 30 # second


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

    current_time = datetime.now()
    current_time_str = current_time.strftime("%H:%M:%S")

    can_check_in = False
    can_check_out = False
    has_records = False

    for row in reversed(rows):
        if row['Name'] != name:
            continue

        has_records = True

        if row['Check-out Time'] == '':
            check_in_time = datetime.strptime(row['Check-in Time'], "%H:%M:%S")
            check_in_time = check_in_time.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
            
            if current_time - check_in_time >= timedelta(seconds=CHECK_OUT_DELAY): # default 30 sec
                can_check_out = True
                row['Check-out Time'] = current_time_str
            break

        if row['Check-in Time'] != '' and row['Check-out Time'] != '':
            check_out_time = datetime.strptime(row['Check-out Time'], "%H:%M:%S")
            check_out_time = check_out_time.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
            
            if current_time - check_out_time >= timedelta(seconds=CHECK_IN_DELAY): # default 30 sec
                can_check_in = True
            break

    # Write the updated rows back to the CSV file
    if can_check_out:
        write_to_csv(rows=rows, row=None, write_header=True)
        print(f"{name} checked out at {current_time_str}.")
    elif can_check_in or not has_records:
        row = {'Student ID': student_id, 'Name': name, 'Check-in Time': current_time_str, 'Check-out Time': ''}
        write_to_csv(rows=None, row=row, write_header=False)
        print(f"{name} checked in at {current_time_str}.")


def get_last_seen(name):
    # Load the CSV file content into a list of dictionaries
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    last_seen_time = None
    status = None

    # Iterate over the rows in reverse order
    for row in reversed(rows):
        if row['Name'] != name:
            continue

        # If a check-out time is found, compare it with the last seen time
        if row['Check-out Time']:
            check_out_time = datetime.strptime(row['Check-out Time'], "%H:%M:%S")
            if not last_seen_time or check_out_time > last_seen_time:
                last_seen_time = check_out_time
                status = "check-out"

        # If a check-in time is found, compare it with the last seen time
        if row['Check-in Time']:
            check_in_time = datetime.strptime(row['Check-in Time'], "%H:%M:%S")
            if not last_seen_time or check_in_time > last_seen_time:
                last_seen_time = check_in_time
                status = "check-in"

        # If both check-in and check-out times are found, break the loop
        if row['Check-in Time'] and row['Check-out Time']:
            break

    # Convert the last seen time to a string
    if last_seen_time:
        last_seen_time = last_seen_time.strftime("%H:%M:%S")

    return last_seen_time, status
