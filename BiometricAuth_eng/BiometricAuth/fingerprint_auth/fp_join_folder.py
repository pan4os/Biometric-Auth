import numpy as np
import skimage.morphology
import os
import cv2
from django.conf import settings

import BiometricAuth.models
from BiometricAuth.utils import check_and_create_folder, get_fingerprint_skelet_path
from PIL import Image

def fp_join_folder(image=None, user_id=None):
    folder = get_fingerprint_skelet_path(user_id)
    check_and_create_folder(folder)

    jpeg_img = Image.open(image)

    basename = os.path.basename(image.name)

    out_file = os.path.join(folder, "{}".format(basename))
    jpeg_img.save(out_file)
    fingerprint_image_deleted = os.listdir(folder)
    find_deleted_fingerprint(user_id)
    fingerprint_image = os.listdir(find_deleted_fingerprint(user_id))
    fingerprint_img = []
    for i in range(int(len(fingerprint_image)-1)):
        for j in range(int(len(fingerprint_image_deleted))):
            if(fingerprint_image[i]==fingerprint_image_deleted[j]):
                fingerprint_img.append(fingerprint_image_deleted[j])
    result=list(set(fingerprint_image_deleted) - set(fingerprint_img))
    for i in range(len(result)):
        os.remove(folder + result[i])



def find_deleted_fingerprint(user_id=None):
    fingerprint_folder_name = 'biometric_data\\user_{}\\fingerprint\\'.format(user_id)
    return os.path.join(settings.MEDIA_ROOT, fingerprint_folder_name)
    fingerprint_image = os.listdir(find_deleted_fingerprint(user_id))
    for i in range(len(fingerprint_image)):
        print(fingerprint_image[i])
    #out_file = cv2.imwrite(folder + basename, (255*enhanced_img))
