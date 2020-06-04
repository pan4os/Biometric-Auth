import cv2
from PIL import Image
import numpy as np

from .FingerPrintComparator import FingerPrintComparator

def fingerprint_verify(image1, image2):

        open_cv_image = np.array(image1)
        opencv_image=cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
        open_cv_image_1 = np.array(image2)
        opencv_image_1=cv2.cvtColor(open_cv_image_1, cv2.COLOR_RGB2BGR)
        finger_print_comparator = FingerPrintComparator()
        if finger_print_comparator.compare_finger_prints(opencv_image, opencv_image_1):
            return True
        else:
            return False
