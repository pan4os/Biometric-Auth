import cv2
import numpy as np

from BiometricAuth.fingerprint_auth.image_enhance import image_enhance
from PIL import Image

class ImageEnhancer:

    def get_enhance_from_image(self, img):
        #img_1 = Image.open(img)
        #open_cv_image = np.array(img_1)
        #opencv_image=cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        rows, cols = np.shape(img)
        aspect_ratio = np.double(rows) / np.double(cols)

        new_rows = 350  # randomly selected number
        new_cols = new_rows / aspect_ratio

        img = cv2.resize(img, (np.int(new_cols), np.int(new_rows)))

        return (255 * image_enhance(img))
