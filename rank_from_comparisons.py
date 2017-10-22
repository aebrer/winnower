import random
import glob
import os
import elo

elo = elo.Elo(50, rating_class=elo.CountedRating, initial=1200, beta=400)

photo_dir = "unranked_sets/"
assert os.path.isdir(photo_dir)

filelist = glob.glob(photo_dir + '*.jpg')

scores = {}  # assign random scores
for file in filelist:
    scores[file] = elo.create_rating()

with open("compare_results.csv") as comparisons:
    for line in comparisons:
        cols = line.split(",")
        if int(cols[2]) == 0:
            scores[cols[0]], scores[cols[1]] = elo.rate_1vs1(scores[cols[0]], scores[cols[1]])
        elif int(cols[2]) == 1:
            scores[cols[1]], scores[cols[0]] = elo.rate_1vs1(scores[cols[1]], scores[cols[0]])
        elif int(cols[2]) == 2:
            scores[cols[0]], scores[cols[1]] = elo.rate_1vs1(scores[cols[0]], scores[cols[1]], 1)


with open("ranked_sets.csv", "w") as ranked_output:
    for file in scores:
        ranked_output.write(str(file) + "," + str(scores[file].value) + "," + str(scores[file].times) + "\n")

