import csv
import os
from datetime import datetime

# Function to handle writing attendance to CSV
def write_attendance_to_csv(student_id, student_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('attendance.csv', 'a', newline='') as csvfile:
        fieldnames = ['TimeStamp', 'StudentID', 'StudentName']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if os.stat('attendance.csv').st_size == 0:
            writer.writeheader()  # Write header if file is empty
        writer.writerow({'TimeStamp': timestamp, 'StudentID': student_id, 'StudentName': student_name})

# Function to read student names from CSV based on ID
def lookup_student_name(student_id):
    with open('student_info.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ID'] == student_id:
                return row['Name']
    return "Unknown"

# Function to add or update student info in the CSV
def add_student_info(student_id, student_name):
    data = {'ID': student_id, 'Name': student_name}
    with open('student_info.csv', 'a+', newline='') as csvfile:
        fieldnames = ['ID', 'Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvfile.seek(0)
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ID'] == student_id:
                print("Student ID already exists.")
                return
        writer.writerow(data) 

