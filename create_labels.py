"""
This script is to convert the ranked list into sets of files to train on.
By default, it takes the top third and the bottom third, and labels them into "like" and "dislike" sets.
"""


import numpy as np
from shutil import copyfile
import glob
import os

photo_dir = "ranked_sets/like/"
assert os.path.isdir(photo_dir)
filelist = glob.glob(photo_dir + '*.jpg')
for file in filelist:
    os.remove(file)

photo_dir = "ranked_sets/dislike/"
assert os.path.isdir(photo_dir)
filelist = glob.glob(photo_dir + '*.jpg')
for file in filelist:
    os.remove(file)
#
# photo_dir = "ranked_sets/neutral/"
# assert os.path.isdir(photo_dir)
# filelist = glob.glob(photo_dir + '*.jpg')
# for file in filelist:
#     os.remove(file)

ranked_sets = open("ranked_sets.csv", "r")

files = []
scores = []

# process the CSV
for line in ranked_sets:
    line = line.rstrip()
    files.append(line.split(",")[0])
    scores.append(float(line.split(",")[1]))

scores = np.array(scores)
# files = np.array(files)
# print(scores)
#
# print(np.max(scores), np.min(scores), np.median(scores), np.mean(scores), np.std(scores), len(scores))
# print(np.median(scores) + np.std(scores), np.median(scores) - np.std(scores))

files, scores = (list(t) for t in zip(*sorted(zip(files, scores))))

# get the sets
n = len(files)
good_limit = int(n/3)
bad_limit = n - good_limit

# print(good_limit, bad_limit)

# good_limit = np.mean(scores) + 0.4 * np.std(scores)
# bad_limit = np.mean(scores) - 0.4 * np.std(scores)
#
# good_scores = scores[scores >= good_limit]
# bad_scores = scores[scores <= bad_limit]
#
# print(len(good_scores), len(bad_scores))
#

# move the right sets into the right folders
good_files = files[0:good_limit]
neutral_files = files[good_limit:bad_limit]
bad_files = files[bad_limit:n]
# print(len(good_files), len(bad_files), len(neutral_files))

for file in good_files:
    filename = file.split("/")[1]
    copyfile(file, "ranked_sets/like/" + filename)

for file in bad_files:
    filename = file.split("/")[1]
    copyfile(file, "ranked_sets/dislike/" + filename)
#
# for file in neutral_files:
#     filename = file.split("/")[1]
#     copyfile(file, "ranked_sets/neutral/" + filename)
