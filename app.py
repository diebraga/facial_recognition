import sys
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import shutil
import os
import cv2
import face_recognition
import numpy as np
import math
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


def encode_faces():
    known_face_encodings = []
    known_face_names = []

    for image in os.listdir('faces'):
        if image.startswith('.'):
            continue
        face_image = face_recognition.load_image_file(f"faces/{image}")
        face_encoding = face_recognition.face_encodings(face_image)[0]

        known_face_encodings.append(face_encoding)
        known_face_names.append(image)

    return known_face_encodings, known_face_names

@app.post("/face_recognition")
async def face_recognition_api(image: UploadFile = File(...)):
    known_face_encodings, known_face_names = encode_faces()

    # Save the uploaded image temporarily
    with open("temp_image.jpg", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Load the image
    frame = cv2.imread("temp_image.jpg")

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        confidence = '???'

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            confidence = face_confidence(face_distances[best_match_index])

        face_names.append(f'{name} ({confidence})')

    results = []
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        results.append({
            "name": name,
            "confidence": confidence,
            "top": top,
            "right": right,
            "bottom": bottom,
            "left": left
        })

    return {"results": results}
