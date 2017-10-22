import random
import glob
import os

photo_dir = "unranked_sets/"
assert os.path.isdir(photo_dir)

MIN_SCORE, MAX_SCORE = 0.0, 5.0
N_ITERATIONS = 100000  # for search stopping condition


def random_score():
    # generate random score between MIN_SCORE and MAX_SCORE
    return MIN_SCORE+random.random()*(MAX_SCORE-MIN_SCORE)

filelist = glob.glob(photo_dir + '*.jpg')
num_photos = len(filelist)

ratings = []  #tuples of (elem_a, elem_b), representing rating a<b

with open("compare_results.csv") as comparisons:
    for line in comparisons:
        cols = line.split(",")
        if int(cols[2]) == 0:
            ratings.append((cols[1],cols[0]))
        else:
            ratings.append((cols[0], cols[1]))

scores = {}  # assign random scores
for file in filelist:
    scores[file] = random_score()


def evaluate_condition(rating):
    # is a user-provided rating true, given the current scores
    return scores[rating[0]] < scores[rating[1]]


def metric():
    # number of true conditions
    return sum(map(evaluate_condition, ratings))

no_improvement_iterations = 0  # number of successive iterations where there has been no improvement
current_score = metric()

while no_improvement_iterations < N_ITERATIONS:
    rand_key = random.choice(list(scores))
    new_value = random_score()
    old_value = scores[rand_key]
    scores[rand_key] = new_value
    new_score = metric()
    if new_score <= current_score:
        scores[rand_key] = old_value
        no_improvement_iterations += 1
    else:
        no_improvement_iterations = 0
        current_score = new_score

with open("ranked_sets.csv", "w") as ranked_output:
    for file in scores:
        ranked_output.write(str(file) + "," + str(scores[file]) + "\n")
