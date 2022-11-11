import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys

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
    return labeled_img

def main():
    import time
    start_time = time.time()
    # Open the image
    image_path = sys.argv[1]
    start_time = time.time()
    img = cv2.imread(image_path, 0)
    # print(img.size)
    # ensure binary image, use THRESH_BINARY_INV to label for black pixel (back ground is white).
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)[1]
    num_labels, labels_im = cv2.connectedComponents(img, connectivity=CONNECTIVITY_8)

    labeled_img = imshow_components(labels_im)
    print('Algorithms: Union Find (OpenCV)')
    print('Image size: {}'.format(img.shape[::-1]))
    print('Number of Label: {}'.format(num_labels-1))   # opencv include label of background
    print('Processing Time:', time.time() - start_time)
    plt.imshow(labeled_img)
    plt.show()

if __name__ == "__main__":
    main()