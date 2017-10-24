import random
import glob
import os


# definition for a type of dictionary that will allow new dictionaries to
# be added on demand
class NestedDict(dict):
    def __missing__(self, key):
        self[key] = NestedDict()
        return self[key]


def win_calc(competitor, records, alpha):

    provisional_score = 0.0
    losers = []

    for challenger in records[competitor]:
        # record a win
        if records[competitor][challenger] == "win":
            provisional_score += 1.0
            losers.append(challenger)

    # update the score based on alpha
    provisional_score = provisional_score * alpha

    # check for base case here
    if provisional_score <= 0.01:
        win_score = provisional_score
        return win_score

    else:
        # now update the score based on competitor scores
        alpha = alpha * 0.9
        for challenger in losers:
            provisional_score = provisional_score + win_calc(challenger, records, alpha)

        win_score = provisional_score

    return win_score


def lose_calc(competitor, records, alpha):

    provisional_score = 0.0
    winners = []

    for challenger in records[competitor]:
        # record a loss
        if records[competitor][challenger] == "loss":
            provisional_score -= 1.0
            winners.append(challenger)

    # update the score based on alpha
    provisional_score = provisional_score * alpha

    # check for base case here
    if provisional_score >= -0.01:
        lose_score = provisional_score
        return lose_score

    else:
        # now update the score based on competitor scores
        alpha = alpha * 0.9
        for challenger in winners:
            provisional_score = provisional_score + lose_calc(challenger, records, alpha)

        lose_score = provisional_score

    return lose_score


def draw_calc(competitor, records, pre_draw_scores):

    draw_score = 0.0

    for challenger in records[competitor]:
        if records[competitor][challenger] == "draw":
            # a draw here represents a situation where there is enough uncertainty to make comparison difficult
            # it does not mean that they are actually equal
            draw_score = ((pre_draw_scores[challenger] - pre_draw_scores[competitor]) / random.uniform(1.9, 2.1))


    return draw_score


photo_dir = "unranked_sets/"
assert os.path.isdir(photo_dir)
filelist = glob.glob(photo_dir + '*.jpg')


comparisons = NestedDict()
with open("compare_results.csv") as comparison_file:
    for line in comparison_file:

        cols = line.split(",")
        A =cols[0]
        B = cols[1]
        outcome = int(cols[2])

        if outcome == 0:
            comparisons[A][B] = "win"
            comparisons[B][A] = "loss"
        elif outcome == 1:
            comparisons[A][B] = "loss"
            comparisons[B][A] = "win"
        elif outcome == 2:
            comparisons[A][B] = "draw"
            comparisons[B][A] = "draw"

win_scores = NestedDict()
lose_scores = NestedDict()
pre_draw_scores = NestedDict()
final_scores = NestedDict()

for file in filelist:
    win_scores[file] = win_calc(file, comparisons, 1.0)
    lose_scores[file] = lose_calc(file, comparisons, 1.0)
    pre_draw_scores[file] = win_scores[file] + lose_scores[file]

for file in filelist:
    final_scores[file] = pre_draw_scores[file] + draw_calc(file, comparisons, pre_draw_scores)

with open("ranked_sets.csv", "w") as ranked_output:
    for file in filelist:
        ranked_output.write(str(file) + "," + str(final_scores[file]) + "\n")

