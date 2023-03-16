import os
import face_recognition

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
