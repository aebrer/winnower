"""
A script to just take every image in the unranked_sets, and just move them to the right folder (like, dislike, or neutral)
"""

import matplotlib.pyplot as plt
from PIL import Image as im
import os
import glob
import random
from shutil import copyfile, move



class Display(object):

    """
    Given two photos, displays them with Matplotlib and provides a graphical
    means of choosing the better photo.

    Click on the select button to pick the better photo.

    ~OR~

    Press the left or right arrow key to pick the better photo.

    """

    def __init__(self, f1, title = None, figsize = None):

        self.f1 = f1

        im1 = im.open(f1)

        if figsize is None:
            figsize = [5,5]

        fig = plt.figure(figsize=figsize)

        h = 10

        ax11 = plt.subplot2grid((h,1), (0,0), rowspan = h)

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

        for ax in [ax11]:
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
            filename = f1.split("/")[1]
            print(filename)
            move(f1, "manual_sort_single/dislike/" + filename)
            plt.close(self._fig)

        elif event.key == 'right':
            filename = f1.split("/")[1]
            print(filename)
            move(f1, "manual_sort_single/like/" + filename)
            plt.close(self._fig)

        elif event.key == 'down':
            filename = f1.split("/")[1]
            print(filename)
            move(f1, "manual_sort_single/neutral/" + filename)
            plt.close(self._fig)

    def _attach_callbacks(self):
        self._fig.canvas.mpl_connect('key_press_event', self._on_key_press)


photo_dir = "unranked_single/"

assert os.path.isdir(photo_dir)

filelist = glob.glob(photo_dir + '*.jpg')
all_existing = list()
all_existing.extend(glob.glob("ranked_single_images/like/*.jpg"))
all_existing.extend(glob.glob("ranked_single_images/dislike/*.jpg"))
all_existing.extend(glob.glob("ranked_single_images/neutral/*.jpg"))
print(len(filelist))
filelist = list(set(filelist) - set(all_existing))
print(len(filelist))
random.shuffle(filelist)
num_photos = len(filelist)
num_files = len(filelist)
counter = 1.0
for f1 in filelist:

    percent = round((counter / float(num_files)) * 100, 2)
    remaining = num_files - counter
    print("Comparing images one-at-a-time:", percent, "percent done,", remaining, "remaining.")

    display = Display(f1)

    counter += 1.0
