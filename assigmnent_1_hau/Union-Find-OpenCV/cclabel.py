import cv2
import numpy as np
import time
from PIL import Image

CONNECTIVITY_4 = 4
CONNECTIVITY_8 = 8


def imshow_components(labels):
    # Map component labels to hue val
    label_hue = np.uint8(179*labels/np.max(labels))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue==0] = 0

    # cv2.imshow('labeled.png', labeled_img)
    # cv2.waitKey()
    return labeled_img

start_time = time.time()

# img = cv2.imread('example.png', 0)
# img = cv2.imread('letters.png', 0)
# img = cv2.imread('bangten.png', 0)
# img = cv2.imread('sticker.png', 0)
img = cv2.imread('bien_so_2.png', 0)
# print(img.size)
# ensure binary image, use THRESH_BINARY_INV to label for black pixel (back ground is white).
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)[1]
num_labels, labels_im = cv2.connectedComponents(img, connectivity=CONNECTIVITY_8)

labeled_img = imshow_components(labels_im)
print('Algorithms: Union Find (OpenCV)')
print('Image size: {}'.format(img.shape[::-1]))
print('Number of Label: {}'.format(num_labels-1))   # opencv include label of background
print('Processing Time:', time.time() - start_time)
cv2.imwrite('result.png', labeled_img)
cv2.imshow('labeled.png', labeled_img)
cv2.waitKey()

