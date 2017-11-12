"""
Will take the high_confidence automatic images, and add them to the sets of training images.
Really creates a lot of bias. It's unclear to me as of now if this is worth it or not. It reduces the number of
some types of false positives, while really securing others.
"""


from shutil import copyfile
import glob


liked = glob.glob("automatically_liked/*.jpg")
for file in liked:
    if float(file.split("_")[4]) > 0.9:
        filename = file.split("/")[1]
        copyfile(file, "ranked_sets/like/" + filename)

disliked = glob.glob("automatically_disliked/*.jpg")
for file in disliked:
    if float(file.split("_")[5]) > 0.9:
        filename = file.split("/")[1]
        copyfile(file, "ranked_sets/dislike/" + filename)


