import numpy as np
from PIL import Image
from union_find import UnionFind
import random
import argparse
import os
# from matplotlib.pyplot as plt


CONNECTIVITY_4 = 4
CONNECTIVITY_8 = 8


def connected_component_labelling(bool_input_image, connectivity_type=CONNECTIVITY_8):
    """
            2 pass algorithm using disjoint-set data structure with Union-Find algorithms to maintain
            record of label equivalences.

            Input: binary image as 2D boolean array.
            Output: 2D integer array of labelled pixels.

            1st pass: label image and record label equivalence classes.
            2nd pass: replace labels with their root labels.

            (optional 3rd pass: Flatten labels so they are consecutive integers starting from 1.)

    """
    if connectivity_type != 4 and connectivity_type != 8:
        raise ValueError("Invalid connectivity type (choose 4 or 8)")

    image_width = len(bool_input_image[0])
    image_height = len(bool_input_image)

    # initialise efficient 2D int array with numpy
    # N.B. numpy matrix addressing syntax: array[y,x]
    labelled_image = np.zeros((image_height, image_width), dtype=np.int16)
    uf = UnionFind()  # initialise union find data structure
    current_label = 1  # initialise label counter

    # 1st Pass: label image and record label equivalences
    for y, row in enumerate(bool_input_image):
        for x, pixel in enumerate(row):

            if pixel == False:
                # Background pixel - leave output pixel value as 0
                pass
            else:
                # Foreground pixel - work out what its label should be

                # Get set of neighbour's labels
                labels = neighbouring_labels(
                    labelled_image, connectivity_type, x, y)

                if not labels:
                    # If no neighbouring foreground pixels, new label -> use current_label
                    labelled_image[y, x] = current_label
                    uf.MakeSet(current_label)  # record label in disjoint set
                    current_label = current_label + 1  # increment for next time

                else:
                    # Pixel is definitely part of a connected component: get smallest label of
                    # neighbours
                    smallest_label = min(labels)
                    labelled_image[y, x] = smallest_label

                    if len(labels) > 1:  # More than one type of label in component -> add
                        # equivalence class
                        for label in labels:
                            uf.Union(uf.GetNode(smallest_label),
                                     uf.GetNode(label))

    # 2nd Pass: replace labels with their root labels
    final_labels = {}
    new_label_number = 1

    for y, row in enumerate(labelled_image):
        for x, pixel_value in enumerate(row):

            if pixel_value > 0:  # Foreground pixel
                # Get element's set's representative value and use as the pixel's new label
                new_label = uf.Find(uf.GetNode(pixel_value)).value
                labelled_image[y, x] = new_label

                # Add label to list of labels used, for 3rd pass (flattening label list)
                if new_label not in final_labels:
                    final_labels[new_label] = new_label_number
                    new_label_number = new_label_number + 1

    # 3rd Pass: flatten label list so labels are consecutive integers starting from 1 (in order
    # of top to bottom, left to right)
    # Different implementation of disjoint-set may remove the need for 3rd pass?
    # for y, row in enumerate(labelled_image):
    #     for x, pixel_value in enumerate(row):

    #         if pixel_value > 0:  # Foreground pixel
    #             labelled_image[y, x] = final_labels[pixel_value]

    return labelled_image


# Private functions ############################################################################
def neighbouring_labels(image, connectivity_type, x, y):
    """
            Gets the set of neighbouring labels of pixel(x,y), depending on the connectivity type.

            Labelling kernel (only includes neighbouring pixels that have already been labelled -
            row above and column to the left):

                    Connectivity 4:
                                n
                             w  x

                    Connectivity 8:
                            nw  n  ne
                             w  x
    """

    labels = set()

    if (connectivity_type == CONNECTIVITY_4) or (connectivity_type == CONNECTIVITY_8):
        # West neighbour
        if x > 0:  # Pixel is not on left edge of image
            west_neighbour = image[y, x-1]
            if west_neighbour > 0:  # It's a labelled pixel
                labels.add(west_neighbour)

        # North neighbour
        if y > 0:  # Pixel is not on top edge of image
            north_neighbour = image[y-1, x]
            if north_neighbour > 0:  # It's a labelled pixel
                labels.add(north_neighbour)

        if connectivity_type == CONNECTIVITY_8:
            # North-West neighbour
            if x > 0 and y > 0:  # pixel is not on left or top edges of image
                northwest_neighbour = image[y-1, x-1]
                if northwest_neighbour > 0:  # it's a labelled pixel
                    labels.add(northwest_neighbour)

            # North-East neighbour
            # Pixel is not on top or right edges of image
            if y > 0 and x < len(image[y]) - 1:
                northeast_neighbour = image[y-1, x+1]
                if northeast_neighbour > 0:  # It's a labelled pixel
                    labels.add(northeast_neighbour)
    else:
        print("Connectivity type not found.")

    return labels


def print_image(img, width, height):
    """
            Prints a 2D array nicely. For debugging.
    """
    colors = []
    colors.append([])
    colors.append([])
    # Displaying distinct components with distinct colors
    coloured_img = Image.new("RGB", (width, height))
    coloured_data = coloured_img.load()

    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] > 0:
                if img[i][j] not in colors[0]:
                    colors[0].append(img[i][j])
                    colors[1].append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

                ind = colors[0].index(img[i][j])
                coloured_data[j, i] = colors[1][ind]
    coloured_img.show()


def image_to_2d_bool_array(image):
    image = image.point(lambda p: p > 190 and 255)
    im2 = image.convert('L')
    arr = np.asarray(im2)
    arr = arr != 255 

    return arr


# Run from Terminal ############################################################################
def parse_args():
    """Defines all arguments.
    Returns
    -------
    args object that contains all the params
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Read directory of list of image inputs')
    parser.add_argument('--root', type=str, help='path to folder containing images.')
    parser.add_argument('--connectivity_type', type=int, default=CONNECTIVITY_8, help='path to folder containing images.')
    parser.add_argument('--exts', nargs='+', default=['.jpeg', '.jpg', '.png'],
                    help='list of acceptable image extensions.')
    args = parser.parse_args()
    args.root = os.path.abspath(args.root)
    return args

def read_image_paths(dir: str, exts: list[str]) -> list[str]:
    """Read path of images from dir input

    Args:
        dir (str): directory of input

    Returns:
        list[str]: list of image inputs
    """
    ls_image_paths = []
    for path, _, files in os.walk(dir, followlinks=True):
        for name_image in files:
            fpath = os.path.join(path, name_image)
            suffix = os.path.splitext(name_image)[1].lower()
            if os.path.isfile(fpath) and (suffix in exts):
                image_path = os.path.join(fpath, name_image)
                ls_image_paths.append(image_path)
        break 
    return ls_image_paths


if __name__ == "__main__":
    args = parse_args()
    connectivity_type = args.connectivity_type

    ls_image_paths = read_image_paths(dir=args.root, exts=args.exts)
    for image_path in ls_image_paths:
        image = Image.open(image_path)
        bool_image = image_to_2d_bool_array(image)
        plt.show(bool_image)
        # result = connected_component_labelling(bool_image, connectivity_type)
        # print_image(result, len(result[0]), len(result))
