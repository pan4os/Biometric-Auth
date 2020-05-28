from django.contrib.auth.models import User
from .models import UserBiometry
from django.contrib.auth.backends import ModelBackend


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
        folder_name = 'user_{}'.format(user.userbiometry.id)
        print(folder_name)
        return True
