import face_recognition
import httpx
from io import BytesIO


async def encode_faces():
    known_face_encodings = []
    known_face_names = []

    image_links = {
        "bill_gates": "https://user-images.githubusercontent.com/52054459/225661748-9b5fa820-08fb-4039-98e6-f61ba5c7c0cc.jpeg",
        "diego_braga": "https://user-images.githubusercontent.com/52054459/225661857-1aabe75c-4519-4f86-969e-d97a05b17616.png",
        "elon_musk": "https://user-images.githubusercontent.com/52054459/225662119-47f2718e-0134-4806-8dcf-952729e3f586.jpeg",
        "jeff_bezos": "https://user-images.githubusercontent.com/52054459/225662155-fee1256a-30b5-43fa-9ebc-15d432fdf8cc.jpeg",
        "mark_zuckerberg": "https://user-images.githubusercontent.com/52054459/225662185-f6892396-2c09-4bb7-8df8-b5f0ff50299b.jpeg"
    }

    async with httpx.AsyncClient() as client:
        for name, url in image_links.items():
            response = await client.get(url)
            image_bytes = BytesIO(response.content)
            face_image = face_recognition.load_image_file(image_bytes)
            face_encoding = face_recognition.face_encodings(face_image)[0]

            known_face_encodings.append(face_encoding)
            known_face_names.append(name)

    return known_face_encodings, known_face_names
