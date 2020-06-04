import os
from django.conf import settings
import base64
from django.core.files.base import ContentFile

def check_and_create_folder(out_folder):
    if os.path.exists(out_folder):
        if os.path.isdir(out_folder):
            print('Каталог найден')
            # print('Список объектов в нем: ',os.listdir(out_folder))
    else:
        print ('Объект не найден')
        try:
            os.mkdir(out_folder)
        except OSError:
            print ("Creation of the directory %s failed" % out_folder)
        else:
            print ("Successfully created the directory %s " % out_folder)

def get_iris_mat_path(user_biometry_id):
    user_iris_folder_name = 'biometric_data/user_{}/iris/mat/'.format(user_biometry_id)
    return os.path.join(settings.MEDIA_ROOT, user_iris_folder_name)

def get_face_mat_path(user_biometry_id):
    user_face_floder_name = 'biometric_data/user_{}/face/'.format(user_biometry_id)
    return os.path.join(settings.MEDIA_ROOT, user_face_floder_name)

def get_fingerprint_skelet_path(user_biometry_id):
    user_fingerprint_folder_name = 'biometric_data/user_{}/fingerprint/skelet/'.format(user_biometry_id)
    return os.path.join(settings.MEDIA_ROOT, user_fingerprint_folder_name)

def get_fingerprint_path(user_biometry_id):
    user_fingerprint_folder_name = 'biometric_data/user_{}/fingerprint/'.format(user_biometry_id)
    return os.path.join(settings.MEDIA_ROOT, user_fingerprint_folder_name)



def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))