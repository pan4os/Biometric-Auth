import face_recognition
import os

def face_verify(image,temp_dir,tolerance=0.6):
    user_image = face_recognition.load_image_file(image)
    for image in os.listdir(temp_dir):
        user_uploaded = face_recognition.load_image_file(os.path.join(temp_dir,image))
        
        try:
            user_image_encoding = face_recognition.face_encodings(user_image)[0]
            user_uploaded_encoding = face_recognition.face_encodings(user_uploaded)[0]
            
            results = face_recognition.compare_faces([user_image_encoding],user_uploaded_encoding,tolerance)
            if results[0]:
                return True
            else:
                return False
        except IndexError:
            return False




    