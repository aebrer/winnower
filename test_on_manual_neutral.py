"""
Show a bunch of neutral images, and what the AI thinks they would be rated. A good test.
"""


import matplotlib.pyplot as plt
from PIL import Image as im
import os
import glob
import random
import label_image



class Display(object):

    """
    Given two photos, displays them with Matplotlib and provides a graphical
    means of choosing the better photo.

    Click on the select button to pick the better photo.

    ~OR~

    Press the left or right arrow key to pick the better photo.

    """

    def __init__(self, f1, choice, prediction, figsize = None):

        self.f1 = f1
        title = str(choice) + ": " + str(prediction)

        im1 = im.open(f1)

        if figsize is None:
            figsize = [20,12]

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
        plt.close(self._fig)


    def _attach_callbacks(self):
        self._fig.canvas.mpl_connect('key_press_event', self._on_key_press)


photo_dir = "manual_sort/neutral/"

assert os.path.isdir(photo_dir)

filelist = glob.glob(photo_dir + '*.jpg')
random.shuffle(filelist)
num_photos = len(filelist)

num_files = len(filelist)
counter = 1.0
for f1 in filelist:

    percent = round((counter / float(num_files)) * 100, 2)
    print("Testing images:", percent, "percent done.")

    results = label_image.use_model("inception_two_class_model.pb", f1)
    choice_type = results[0][0]
    prediction = results[0][1]
    display = Display(f1, choice_type, prediction)


    counter += 1.0
