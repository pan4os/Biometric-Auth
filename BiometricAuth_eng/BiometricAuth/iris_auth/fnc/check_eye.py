# import cv2
# import numpy as np

# def check_eye(file):
#     eye_cascade = cv2.CascadeClassifier('../haarcascade/haarcascade_eye.xml')
#     print(eye_cascade)
#     img = cv2.imread(file)
#     # print('IMG:', img)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     eyes = eye_cascade.detectMultiScale(gray, 1.03, 5)
#     if not eyes:
#         return False
#     return True