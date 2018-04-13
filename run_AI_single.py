"""
This is where the magic happens, the script that actually runs the swiping AI.
"""


from PIL import Image as im
import pynder
import generate_collage
from urllib.request import urlopen
from io import BytesIO
import label_image
import os
import time
import random
import numpy as np


session = pynder.Session(XAuthToken="")
print("Session started..")

import json
print(json.dumps(session._api.profile(), sort_keys=True, indent=2))

counter = 1
# swipe_scores = []  # where to store all the swipe scores

while True:

    users = []

    try:
        print("Getting user and sleeping for some seconds:")
        # matches = session.matches()
        # for match in matches:
        #     if match.user is not None:
        #         users.append(match.user)
        #     else:
        #         continue
        users = session.nearby_users(limit=1)

    except Exception as e:
        print(e)
        continue

    print("Got user, analyzing.")

    for user in users:
        time.sleep(random.randint(1, 5))
        try:
            photos = user.get_photos()
            images = []
            repeat = False
            scores = []
            photo_num = 1
            for photo in photos:
                file = BytesIO(urlopen(photo).read())
                image = im.open(file)
                output_name_single = "unranked_single/" + str(user.id) + "_" + str(user.name) + "_" + str(
                    user.age) + "_" + str(photo_num) + ".jpg"
                image.save(output_name_single)
                results = label_image.use_model("inception_two_class_model_single.pb", output_name_single)
                photo_num += 1

                like = 0.0
                dislike = 0.0
                neutral = 0.0

                for result in results:
                    if result[0] == "like":
                        like = result[1]
                    elif result[0] == "dislike":
                        dislike = result[1]
                    else:
                        neutral += result[1]
                neutral = max(neutral, 0.005)
                score = (like - dislike**2) / neutral
                score = round(score, 3)
                scores.append(score)
                images.append(image)
            collage = generate_collage.generate_collage(images)

            if len(scores) == 0:
                scores.append(-1)

            swipe_score = np.sum(scores)
            swipe_score = round(float(swipe_score), 3)
            # swipe_scores.append(swipe_score)

            # if len(swipe_scores) < 20:
            if swipe_score > 250:
                decision = "super"
            elif swipe_score > 0.5:  # chosen to be a little pickier
                decision = "like"
            else:
                decision = "dislike"
            # else:
            #     if swipe_score > 200:
            #         decision = "super"
            #     elif swipe_score > np.median(swipe_scores):
            #         decision = "like"
            #     else:
            #         decision = "dislike"

            print(user.name, user.age, scores, swipe_score, decision)
            output_name = "single_results/" + str(decision) + "_" + str(swipe_score) + "_" + str(user.name) + "_" + str(
                user.age) + "_" + str(user.id) + "_collage.jpg"
            collage.save(output_name)

            bio_output = "unranked_bio/" + str(user.name) + "_" + str(
                user.age) + "_" + str(user.id) + "_bio.txt"
            with open(bio_output, "w") as biofile:
                if user.bio != "":
                    for line in user.bio:
                        biofile.write(line)

            if decision == "super":
                try:
                    print(user.superlike())
                    try:
                        print(user.like())
                    except:
                        pass
                except:
                    pass
            elif decision == "like":
                print(user.like())
            else:
                print(user.dislike())

        except Exception as e:
            print(e)

    counter += 1
