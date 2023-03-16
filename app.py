from fastapi import FastAPI, File, UploadFile
import shutil
import os
import cv2
import face_recognition
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from utils.face_confidence.face_confidence import face_confidence
from utils.encode_faces.encode_faces import encode_faces

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/face_recognition")
async def face_recognition_api(image: UploadFile = File(...)):
    known_face_encodings, known_face_names = encode_faces()

    # Save the uploaded image to disk
    filename = image.filename
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Load the image
    frame = cv2.imread(filename)

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

        face_names.append(f'{name}')

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

    # Delete the uploaded image file
    os.remove(filename)

    return {"results": results}
