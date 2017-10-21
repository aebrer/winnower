import matplotlib.pyplot as plt
from PIL import Image as im
import os
import glob
from itertools import combinations
import random
import numpy as np


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

    def _attach_callbacks(self):
        self._fig.canvas.mpl_connect('key_press_event', self._on_key_press)


photo_dir = "unranked_sets_testing/"

assert os.path.isdir(photo_dir)

filelist = glob.glob(photo_dir + '*.jpg')
num_photos = len(filelist)
combolist = combinations(filelist, 2)

def random_combination(iterable, num_photos):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    # need to get at least n*log(n) comparisons
    r = int(round(num_photos * np.log(num_photos))) + 1
    indices = random.sample(range(n), r)
    return tuple(pool[i] for i in indices)


rand_combo_list = random_combination(combolist, num_photos)

for f1,f2 in rand_combo_list:
    # print(f1,f2)
    display = Display(f1, f2)


