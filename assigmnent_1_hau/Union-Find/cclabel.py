import numpy as np
from PIL import Image
from union_find import UnionFind
import random
import time

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

    return labelled_image, new_label_number - 1


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
    im2 = image.convert('L').point(lambda p: p > 127 and 255 or 0)
    arr = np.asarray(im2)
    arr = arr != 255 

    return arr


# Run from Terminal ############################################################################
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:  # At least 1 command line parameter
        start_time = time.time()
        image_path = str(sys.argv[1])

        if (len(sys.argv) > 2):  # At least 2
            connectivity_type = int(sys.argv[2])
        else:
            connectivity_type = CONNECTIVITY_8

        image = Image.open(image_path)
        bool_image = image_to_2d_bool_array(image)
        result, label_number = connected_component_labelling(bool_image, connectivity_type)
        
        print('Algorithms: Union-Find')
        print('Image size: {}'.format(image.size))
        print('Number of Label: {}'.format(label_number))
        print('Processing Time:', time.time() - start_time)
        print_image(result, len(result[0]), len(result))
