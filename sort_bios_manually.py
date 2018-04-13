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

    def __init__(self, f1):

        with open(f1, "r") as infile:
            print("\n\n")
            for line in infile.readlines():
                print(line)

        key = ""

        while key != "j" and key != "k" and key != "l":
            key = input()

        if key == 'j':
            filename = f1.split("/")[1]
            move(f1, "manual_sort_bio/dislike/" + filename)

        elif key == 'l':
            filename = f1.split("/")[1]
            move(f1, "manual_sort_bio/like/" + filename)

        elif key == 'k':
            filename = f1.split("/")[1]
            move(f1, "manual_sort_bio/neutral/" + filename)



photo_dir = "unranked_bio/"

assert os.path.isdir(photo_dir)

filelist = glob.glob(photo_dir + '*.txt')
all_existing = list()
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
    print("Comparing bios one-at-a-time:", percent, "percent done,", remaining, "remaining.")

    display = Display(f1)

    counter += 1.0
