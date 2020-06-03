from django.contrib.auth.models import User
from .models import UserBiometry
from PIL import Image
from django.contrib.auth.backends import ModelBackend
from .iris_auth.verify import verify
from .face_auth.face_verify import face_verify
from .utils import get_iris_mat_path, get_fingerprint_skelet_path
from .utils import get_face_mat_path
from .fingerprint_auth.fingerprint_verify import fingerprint_verify
from .fingerprint_auth.fp_join_folder import fp_join_folder
import os

class IrisAuthBackend(ModelBackend):
    '''
    Проферка пользователя по сетчатке глаза
    '''
    def authenticate(self, username=None, password=None, uploaded_iris=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and self.check_iris(user = user, uploaded_iris=uploaded_iris):
                return user
        except User.DoesNotExist:
            print('DOES NOT EXIST')

    def check_iris(self, user=None, uploaded_iris=None):
        folder_path = get_iris_mat_path(user.userbiometry.id)
        uploaded_iris = Image.open(uploaded_iris)
        if verify(uploaded_iris,folder_path):
            return True
        return False

class FaceAuthBackend(ModelBackend):
    '''
    Проферка пользователя по лицу
    '''
    def authenticate(self, username=None, password=None, uploaded_face=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and self.check_face(user = user, uploaded_face=uploaded_face):
                return user
        except User.DoesNotExist:
            print('DOES NOT EXIST')

    def check_face(self, user=None, uploaded_face=None):
        folder_path = get_face_mat_path(user.userbiometry.id)

        if face_verify(uploaded_face,folder_path):
            return True
        return False


class FingerprintAuthBackend(ModelBackend):
    '''
    Проверка пользователя по отпечатку пальца
    '''
    def authenticate(self, username=None, password=None, uploaded_fingerprint=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and self.check_fingerprint(user = user, uploaded_fingerprint=uploaded_fingerprint):
                return user
        except User.DoesNotExist:
            print('DOES NOT EXIST')

    def check_fingerprint(self, user=None, uploaded_fingerprint=None):
        fingerprint_image = os.listdir(get_fingerprint_skelet_path(user.userbiometry.id))
        for i in range(len(fingerprint_image)):
            folder_path = Image.open(str(get_fingerprint_skelet_path(user.userbiometry.id)) + str(fingerprint_image[i]))
            uploaded_fingerprint_f = Image.open(uploaded_fingerprint)
            if fingerprint_verify(uploaded_fingerprint_f, folder_path):
                return True
            else:
                pass
        return False
