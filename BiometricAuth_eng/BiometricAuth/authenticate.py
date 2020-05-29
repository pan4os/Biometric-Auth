from django.contrib.auth.models import User
from .models import UserBiometry
from PIL import Image
from django.contrib.auth.backends import ModelBackend
from .iris_auth.verify import verify
from django.conf import settings
import os

class IrisAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, uploaded_iris=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and self.check_iris(user = user, uploaded_iris=uploaded_iris):                                     
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            # User().set_password(password)
            print('DOES NOT EXIST')

    def check_iris(self, user=None, uploaded_iris=None):
        user_iris_folder_name = 'biometric_data/user_{}/iris/mat/'.format(user.userbiometry.id)
        folder_path = os.path.join(settings.MEDIA_ROOT, user_iris_folder_name)
        # img = Image.open(folder_path+'/001_1_2.jpg')
        # print(img)
        print('TYPE: ', type(uploaded_iris))
        uploaded_iris = Image.open(uploaded_iris)
        if verify(uploaded_iris,folder_path):
            return True
        return False
