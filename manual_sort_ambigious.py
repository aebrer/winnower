"""
Get images that confuse the AI, and manually sort them. Goal, to improve the quality of the AI training.
"""


import matplotlib.pyplot as plt
from PIL import Image as im
import glob
from shutil import copyfile



class Display(object):

    def __init__(self, f1, title = None, figsize = None):

        self.f1 = f1

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

        if event.key == 'left':
            filename = f1.split("/")[1]
            copyfile(f1, "ambigious_sorted/dislike/" + filename)
            plt.close(self._fig)

        elif event.key == 'right':
            filename = f1.split("/")[1]
            copyfile(f1, "ambigious_sorted/like/" + filename)
            plt.close(self._fig)

        elif event.key == 'down':
            filename = f1.split("/")[1]
            copyfile(f1, "ambigious_sorted/neutral/" + filename)
            plt.close(self._fig)

    def _attach_callbacks(self):
        self._fig.canvas.mpl_connect('key_press_event', self._on_key_press)



disliked = glob.glob("automatically_disliked/*.jpg")
ambi_dislike = []
for file in disliked:
    if float(file.split("_")[1].split("/")[1]) < 0.6:
        ambi_dislike.append(file)

num_files = len(ambi_dislike)
counter = 1.0
for f1 in ambi_dislike:
    percent = round((counter / float(num_files)) * 100, 2)
    print("Comparing images one-at-a-time:", percent, "percent done.")

    display = Display(f1)

    counter += 1.0

liked = glob.glob("automatically_liked/*.jpg")
ambi_like = []
for file in liked:
    if float(file.split("_")[1].split("/")[1]) < 0.6:
        ambi_like.append(file)

num_files = len(ambi_like)
counter = 1.0
for f1 in ambi_like:
    percent = round((counter / float(num_files)) * 100, 2)
    print("Comparing images one-at-a-time:", percent, "percent done.")

    display = Display(f1)

    counter += 1.0