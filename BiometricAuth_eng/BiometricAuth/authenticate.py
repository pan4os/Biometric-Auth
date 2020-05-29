from django.contrib.auth.models import User
from .models import UserBiometry
from PIL import Image
from django.contrib.auth.backends import ModelBackend
from .iris_auth.verify import verify
from .utils import get_iris_mat_path

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
    pass

class FingerprintAuthBackend(ModelBackend):
    '''
    Проверка пользователя по отпечатку пальца
    '''
    pass