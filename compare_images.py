import matplotlib.pyplot as plt
from PIL import Image as im
import os
import glob
import random

# a display class that will allow us to speed up the comparisons
# left key, left wins, right key right wins, down key is a draw
class Display(object):

    """
    Given two photos, displays them with Matplotlib and provides a graphical
    means of choosing the better photo.

    Click on the select button to pick the better photo.

    ~OR~

    Press the left or right arrow key to pick the better photo.

    """

    def __init__(self, f1, f2, compare_results_file="compare_results.csv", title = None, figsize = None):

        self.compare_results_file = compare_results_file
        self.f1 = f1
        self.f2 = f2

        im1 = im.open(f1)
        im2 = im.open(f2)

        if figsize is None:
            figsize = [20,12]

        fig = plt.figure(figsize=figsize)

        h = 10

        ax11 = plt.subplot2grid((h,2), (0,0), rowspan = h - 1)
        ax12 = plt.subplot2grid((h,2), (0,1), rowspan = h - 1)

        self._fig = fig

        fig.subplots_adjust(
            left = 0.02,
            bottom = 0.02,
            right = 0.98,
            top = 0.98,
            wspace = 0.05,
            hspace = 0,
        )

        ax11.imshow(im1)
        ax12.imshow(im2)

        for ax in [ax11, ax12]:
            ax.set_xticklabels([])
            ax.set_yticklabels([])

            ax.set_xticks([])
            ax.set_yticks([])

        self._attach_callbacks()

        if title:
            fig.suptitle(title, fontsize=20)

        plt.show()

    def _on_key_press(self, event):

        if event.key == 'left':
            with open(self.compare_results_file, "a") as results:
                results.write(str(self.f1) + "," + str(self.f2) + "," + str(0) + "\n")
            plt.close(self._fig)

        elif event.key == 'right':
            with open(self.compare_results_file, "a") as results:
                results.write(str(self.f1) + "," + str(self.f2) + "," + str(1) + "\n")
            plt.close(self._fig)

        elif event.key == 'down':
            with open(self.compare_results_file, "a") as results:
                results.write(str(self.f1) + "," + str(self.f2) + "," + str(2) + "\n")
            plt.close(self._fig)

    def _attach_callbacks(self):
        self._fig.canvas.mpl_connect('key_press_event', self._on_key_press)


# just a convenience
photo_dir = "unranked_sets/"
assert os.path.isdir(photo_dir)

# get all the images to compare
filelist = glob.glob(photo_dir + '*.jpg')
# put them in a random order
random.shuffle(filelist)
# how many are there?
num_photos = len(filelist)

counter = 1.0
# see every photo at least once
for f1 in filelist:

    percent = round((counter / float(num_photos)) * 100, 2)
    print("Comparing images one-at-a-time:", percent, "percent done.")

    # get a random image that isn't the current image
    f2 = f1
    while f2 == f1:
        f2 = random.choice(filelist)
    display = Display(f1, f2)

    counter += 1.0
