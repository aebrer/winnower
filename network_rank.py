"""
A script to take a set of incomplete pairwise comparisons, and recursively "pseudocompare" them, in order to make
a single ranked list.
"""

import glob
import os


# definition for a type of dictionary that will allow new dictionaries to
# be added on demand
class NestedDict(dict):
    def __missing__(self, key):
        self[key] = NestedDict()
        return self[key]

# function to calculate the WIN score
def win_calc(competitor, records, alpha, seen):

    provisional_score = 0.0
    losers = []

    for challenger in records[competitor]:
        if ((competitor, challenger) not in seen) and ((challenger, competitor) not in seen):
            # record a win
            if records[competitor][challenger] == "win":
                provisional_score += 1.0
                losers.append(challenger)
                seen.append((competitor, challenger))
                seen.append((challenger, competitor))
            # if it's a draw, treat is like a win worth no points (and a lower alpha on the next level of depth
            elif records[competitor][challenger] == "draw":
                seen.append((competitor, challenger))
                seen.append((challenger, competitor))
                provisional_score += win_calc(challenger, records, alpha * 0.4, seen)


    # update the score based on alpha
    provisional_score = provisional_score * alpha

    # check for base case here
    # stop recursion if the score is too low
    if provisional_score <= 0.01:
        win_score = provisional_score
        return win_score

    # go through and get the scores of all the wins of each loser
    else:
        # now update the score based on competitor scores
        alpha = alpha * 0.4
        for challenger in losers:
            provisional_score = provisional_score + win_calc(challenger, records, alpha, seen)

        win_score = provisional_score

    return win_score


# same as the win score function, but for losing. It's the same, but in the opposite direction
def lose_calc(competitor, records, alpha, seen):

    provisional_score = 0.0
    winners = []

    for challenger in records[competitor]:
        if ((competitor, challenger) not in seen) and ((challenger, competitor) not in seen):
            # record a loss
            if records[competitor][challenger] == "loss":
                provisional_score -= 1.0
                winners.append(challenger)
                seen.append((competitor, challenger))
                seen.append((challenger, competitor))
            elif records[competitor][challenger] == "draw":
                seen.append((competitor, challenger))
                seen.append((challenger, competitor))
                provisional_score -= lose_calc(challenger, records, alpha * 0.4, seen)


    # update the score based on alpha
    provisional_score = provisional_score * alpha

    # check for base case here
    if provisional_score >= -0.01:
        lose_score = provisional_score
        return lose_score

    else:
        # now update the score based on competitor scores
        alpha = alpha * 0.4
        for challenger in winners:
            provisional_score = provisional_score + lose_calc(challenger, records, alpha, seen)

        lose_score = provisional_score

    return lose_score



# get the filelist of unranked images
photo_dir = "unranked_sets/"
assert os.path.isdir(photo_dir)
filelist = glob.glob(photo_dir + '*.jpg')

# get all the comparisons
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

final_scores = {}

# get a score for each collage in the filelist
for file in filelist:
    if comparisons[file] == {}:
        print("No comparison yet exists for: " + file)
    seen = []
    final_scores[file] = win_calc(file, comparisons, 1.0, seen) + lose_calc(file, comparisons, 1.0, seen)

# save the ranked list as the result
with open("ranked_sets.csv", "w") as ranked_output:
    for file in filelist:
        ranked_output.write(str(file) + "," + str(final_scores[file]) + "\n")

