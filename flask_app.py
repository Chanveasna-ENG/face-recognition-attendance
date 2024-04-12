# server.py
from flask import Flask, render_template, Response, jsonify
import cv2
import os
import base64
from datetime import datetime
import numpy as np
import face_recognition as face
import PIL.Image as Image


def load_known_faces():
    # list directory
    for filename in os.listdir(known_faces_dir):
        # get name and extension
        name, ext = os.path.splitext(filename)
        # check if it is an image
        if ext in ['.jpg', '.jpeg', '.png']:
            image = face.load_image_file(os.path.join(known_faces_dir, filename))
            encoding = face.face_encodings(image)[0]
            # add to dictionary
            known_faces[name] = encoding


def recognize(unknown_encoding):
    # Compare face encodings
    results = face.compare_faces(list(known_faces.values()), unknown_encoding, tolerance=0.5)
    # Get the name of the person using the results
    for name, result in zip(known_faces.keys(), results):
        if result:
            return name

    return 'Unknown'


def recognize2(unknown_encoding):
    # Calculate face distance
    face_distances = face.face_distance(list(known_faces.values()), unknown_encoding)
    # Get the index of the best match
    best_match_index = np.argmin(face_distances)
    # Compare face encodings
    results = face.compare_faces(list(known_faces.values()), unknown_encoding, tolerance=0.5)

    # Check if the best match is a match
    if results[best_match_index]:
        name = list(known_faces.keys())[best_match_index]
        return name

    return 'Unknown'


# Get a reference to default webcame
video_capture = cv2.VideoCapture(0)

script_dir = os.path.dirname(os.path.abspath(__file__))
known_faces_dir = os.path.join(script_dir, 'known_faces')
unknown_image_path = os.path.join(script_dir, 'static', 'Unknown.jpeg')
blank_image_path = os.path.join(script_dir, 'static', 'blank.jpeg')

known_faces = {}
load_known_faces()
face_names = []

# Flask App
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    global face_names

    frame_counter = 0
    while True:
        # Grab every single frame of video
        ret, frame = video_capture.read()

        # Only process every 30th frame of video to save time
        # user must stay still for a while for it to capture
        if frame_counter % 30 == 0:
            # Reset frame counter
            frame_counter = 0
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
            # Find all the faces in the current frame of video
            face_locations = face.face_locations(small_frame)
            # Encode the faces in the current frame of video by their location
            face_encodings = face.face_encodings(small_frame, face_locations)
            # Recognize the faces and store the names
            face_names = [recognize2(face_encoding) for face_encoding in face_encodings]

        # Increment frame counter
        frame_counter += 1


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(img=frame, 
                        pt1=(left, top), 
                        pt2=(right, bottom), 
                        color=(0, 0, 255), 
                        thickness=2)

            # Draw a label with a name below the face
            cv2.rectangle(img=frame, 
                        pt1=(left, bottom - 35), 
                        pt2=(right, bottom), 
                        color=(0, 0, 255), 
                        thickness=cv2.FILLED)

            cv2.putText(img=frame, 
                        text=name, 
                        org=(left + 6, bottom - 6), 
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, 
                        fontScale=1.0, 
                        color=(255, 255, 255), 
                        thickness=1)

        # Displaying counter
        cv2.putText(img=frame, 
                    text=str(frame_counter), 
                    org=(20, 20), 
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, 
                    fontScale=1.0, 
                    color=(255, 255, 255), 
                    thickness=1)

        # Convert the frame to .jpg file for streaming
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def encode_image_base64(image_path):
    img = Image.open(image_path).convert("RGB")
    numpy_img = np.array(img)

    # Convert color space from RGB to BGR
    numpy_img = cv2.cvtColor(numpy_img, cv2.COLOR_RGB2BGR)

    ret, buffer = cv2.imencode('.jpg', numpy_img)
    byte_arr = buffer.tobytes()

    return base64.b64encode(byte_arr).decode('utf-8')


def find_img(name):
    for filename in os.listdir(known_faces_dir):
        if filename.startswith(f"{name}."):
            return f'{known_faces_dir}/{filename}'
    return blank_image_path


@app.route('/recognized_face')
def recognized_face():
    global face_names
    data = []

    for name in face_names:
        image_path = unknown_image_path if name == 'Unknown' else find_img(name)
        
        data.append({
            'name': name, 
            'image': encode_image_base64(image_path),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    if data:
        return jsonify(data)
    else:
        return jsonify([{
            'name': 'Name', 
            'image': encode_image_base64(blank_image_path),
            'timestamp': 'Timestamp'
            }])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)