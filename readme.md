# This is Face Recognition Attendance System using Python

We are Team 2 from AUPP IT Club. In spring, semester 2024, we are working on a project to develop a Face Recognition Attendance System using Python. The team members are:
- ENG Chanveasna
- HEANG Tong
- HENG Shito
- HORNG Linda
- DIEP Thavy

This project is mainly for the purpose of learning and practicing Python programming language. We are using the following libraries:
- [OpenCV](https://opencv.org/)
- [Face Recognition](https://github.com/ageitgey/face_recognition)
- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://numpy.org/)
- [csv](https://docs.python.org/3/library/csv.html)

The project is divided into 3 main parts:
1. Face Detection & Face Recognition
2. Attendance System
3. User Interface

We are using the following steps to develop the project:
1. Research
2. Planning
3. Coding
4. Testing
5. Documentation
6. Future Development & Limitation

## Research
We found some similar project on github that utilize the same libraries. We are using the following projects as reference:
1. [Face Recognition](https://github.com/ageitgey/face_recognition)
2. [Face Attendance System](https://github.com/computervisioneng/face-atendance-system)
3. [Face_Recognition_Project](https://github.com/Chando0185/face_recognition_project)

## Planning
We have planned the project and divided the tasks among the team members. We have created a project plan and a timeline to follow.

## Coding
The code is done, we have three part to this. The UI, Core system, and Database.
Besides, we also add some simple optimization to the program, by only recognize the face once every 50 frames and resize the image to 4 times smaller for fast recognition. 

## Testing
We have coded the program and tested it on windows machine and ubuntu machine.
As we tested it, we noticed that the face_recognition library is slow and not working well on windows machine. Even if we can install dlib and face_recognition using pre-build wheel It is still slow, since the library itself is not officially support on windows.
So, for best performance we recommend using Ubuntu or other linux system to run this program.

## Running

### Clone
```Bash
$ git clone https://github.com/Chanveasna-ENG/face-recognition-attendance.git
```

### Change Directory
```Bash
$ cd face-recognition-attendance
```

### Install dependencies
```Bash
$ pip3 install -r requirements.txt
```

### Run the program
```Bash
$ flask --app=flask_app.py run
```

## Documentation
1. User can add new face by copying the image with student's name as file's name to the `known_faces` folder and run the program.
2. The only thing that user may need to change is the time dalay for check-in and check-out. The default is 30 seconds for both check-in and check-out in `Database.py` file.
3. The program will create a csv file to store the attendance record. The file will be created in `attendance` directory in program's directory.
4. User can change the delay for face recognition in `flask_app.py` file. The default is 50 frames.

## Future Development & Limitation
- This one doesn't have spoofing detection yet, so people can use other people image to login
- For simplicity sake, we build database system using csv file, which is not efficience for large database. Then we actually make it more complicated as some of the function could be accomplish with one SQL command. 
- We didn't implement the Student ID yet. For real school system, the ID is important because some students may have the same name.
- The UI looks good, but may need some improvement.
- We haven't test on other system, especially for raspberry pi, which is the main target for this project. We won't be able to test it since we don't have the hardware.

__To Be Continue...__