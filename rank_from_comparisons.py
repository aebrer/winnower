import random
import glob
import os
import elo

photo_dir = "unranked_sets/"
assert os.path.isdir(photo_dir)

filelist = glob.glob(photo_dir + '*.jpg')

scores = {}  # assign random scores
for file in filelist:
    scores[file] = 1200

with open("compare_results.csv") as comparisons:
    for line in comparisons:
        cols = line.split(",")
        if int(cols[2]) == 0:
            scores[cols[0]], scores[cols[1]] = elo.rate_1vs1(scores[cols[0]], scores[cols[1]])
        else:
            scores[cols[1]], scores[cols[0]] = elo.rate_1vs1(scores[cols[1]], scores[cols[0]])

with open("ranked_sets.csv", "w") as ranked_output:
    for file in scores:
        ranked_output.write(str(file) + "," + str(scores[file]) + "\n")

