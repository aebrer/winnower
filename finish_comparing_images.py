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

        elif event.key == 'down':
            with open(self.compare_results_file, "a") as results:
                results.write(str(self.f1) + "," + str(self.f2) + "," + str(2) + "\n")
            plt.close(self._fig)

    def _attach_callbacks(self):
        self._fig.canvas.mpl_connect('key_press_event', self._on_key_press)


photo_dir = "unranked_sets/"

assert os.path.isdir(photo_dir)

filelist = glob.glob(photo_dir + '*.jpg')
random.shuffle(filelist)
num_photos = len(filelist)

scores = {}

with open("ranked_sets.csv", "r") as ranked_list:
    for line in ranked_list:
        line = line.rstrip()
        file = line.split(",")[0]
        score = abs(float(line.split(",")[1]))

        int_score = round(float(score))
        float_score = float(score)
        diff = abs(float_score - int_score)

        if diff == 0:
            f2 = random.choice(filelist)
            while f2 == file:
                f2 = random.choice(filelist)
            display = Display(file, f2)

        if score not in scores:
            scores[score] = [file]
        else:
            scores[score].append(file)

total_len = len(scores)
counter = 1.0

for score in scores:
    percent = round((counter / float(total_len)) * 100, 2)
    print("Now comparing scores:", percent, "percent done.")
    if len(scores[score]) > 1:
        images = len(scores[score])
        image_count = 1.0
        for file in scores[score]:
            percent = round((image_count / float(images)) * 100, 2)
            print("Now comparing images within this score:", percent, "percent done.")
            f2 = random.choice(filelist)
            while f2 in scores[score]:
                f2 = random.choice(filelist)
            display = Display(file, f2)
            image_count += 1.0
    counter += 1.0

