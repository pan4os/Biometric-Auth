import cv2
import numpy as np


from BiometricAuth.fingerprint_auth.ImageEnhancer import ImageEnhancer
from BiometricAuth.fingerprint_auth.getTerminationBifurcation import get_descriptors


class FingerPrintComparator:

    def __init__(self):
        self.image_enhancer = ImageEnhancer()

    def compare_finger_prints(self, first_finger_print, second_finger_print):

        first_finger_print = self.image_enhancer.get_enhance_from_image(first_finger_print)
        second_finger_print = self.image_enhancer.get_enhance_from_image(second_finger_print)

        return self.__is_finger_prints_matches(first_finger_print, second_finger_print)

    def __is_finger_prints_matches(self, first_finger_print, second_finger_print):

        first_finger_print = np.uint8(first_finger_print > 128)
        second_finger_print = np.uint8(second_finger_print > 128)
        kp1, des1 = get_descriptors(first_finger_print)
        kp2, des2 = get_descriptors(second_finger_print)

        # Matching between descriptors
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = sorted(bf.match(des1, des2), key=lambda match: match.distance)

        # Calculate score
        score = 0
        for match in matches:
            score += match.distance
        score_threshold = 43.9
        print(score / len(matches))
        if score / len(matches) < score_threshold:
            return True
        else:
            return False
