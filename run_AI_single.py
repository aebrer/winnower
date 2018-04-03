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


session = pynder.Session(XAuthToken="NULL")
print("Session started..")

import json
print(json.dumps(session._api.profile(), sort_keys=True, indent=2))

counter = 1
swipe_scores = []  # where to store all the swipe scores

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
        time.sleep(random.randint(3, 15))
        try:
            photos = user.get_photos()
            images = []
            repeat = False
            scores = []
            for photo in photos:
                file = BytesIO(urlopen(photo).read())
                image = im.open(file)
                image.save("tmp.jpg")
                results = label_image.use_model("inception_two_class_model_single.pb", "tmp.jpg")
                os.remove("tmp.jpg")

                like = 0.0
                dislike = 0.0
                neutral = 0.0

                for result in results:
                    if result[0] == "like":
                        like = result[1]
                    if result[0] == "dislike":
                        dislike = result[1]
                    if result[0] == "neutral":
                        neutral = result[1]

                score = like / (np.mean([dislike, neutral]))
                scores.append(score)
                images.append(image)
            collage = generate_collage.generate_collage(images)

            if len(scores) == 0:
                scores.append(-1)

            swipe_score = np.sum(scores)
            swipe_scores.append(swipe_score)

            if len(swipe_scores) < 20:
                if swipe_score > 3:
                    decision = True
                else:
                    decision = False
            else:
                if swipe_score > np.median(swipe_scores):
                    decision = True
                else:
                    decision = False

            if decision:
                print(user.like())
            else:
                print(user.dislike())

            print(user.name, user.age, scores, swipe_score, decision)
            output_name = "single_results/" + str(decision) + "_" + str(swipe_score) + "_" + str(user.name) + "_" + str(
                user.age) + "_" + str(user.id) + "_collage.jpg"
            collage.save(output_name)

        except Exception as e:
            print(e)
