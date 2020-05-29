import os
from django.conf import settings

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