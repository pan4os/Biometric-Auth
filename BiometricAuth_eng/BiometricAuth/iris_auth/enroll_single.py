import argparse, os
from time import time
from scipy.io import savemat

from .fnc.extractFeature import extractFeature
from BiometricAuth.utils import check_and_create_folder, get_iris_mat_path
from PIL import Image
import numpy as np

# from .fnc.check_eye import check_eye

def enroll_single(image=None, user_id=None):
    folder = get_iris_mat_path(user_id)
    check_and_create_folder(folder)
    # print('\tFolder: ', folder)
    jpeg_img = Image.open(image)
    template, mask = extractFeature(im=np.array(jpeg_img))
    # print('\tFile: ', file)
    basename = os.path.basename(image.name)
    # print('\tBase name: ', basename)
    out_file = os.path.join(folder, "{}.mat".format(basename))
    print('\tIris out file: ', out_file)
    savemat(out_file, mdict={'template':template, 'mask':mask})