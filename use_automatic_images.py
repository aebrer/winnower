from numpy import array, linspace
from sklearn.neighbors.kde import KernelDensity
from matplotlib.pyplot import plot
import numpy as np
from shutil import copyfile
import glob
import os


liked = glob.glob("automatically_liked/*.jpg")
for file in liked:
    if float(file.split("_")[4]) > 0.8:
        filename = file.split("/")[1]
        copyfile(file, "ranked_sets/like/" + filename)

disliked = glob.glob("automatically_disliked/*.jpg")
for file in disliked:
    if float(file.split("_")[4]) > 0.8:
        filename = file.split("/")[1]
        copyfile(file, "ranked_sets/dislike/" + filename)


