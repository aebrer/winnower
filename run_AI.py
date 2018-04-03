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


session = pynder.Session(XAuthToken="NULL")
print("Session started..")

import json
print(json.dumps(session._api.profile(), sort_keys=True, indent=2))

counter = 1

while True:

    users = []

    try:
        print("Getting user and sleeping for some seconds:")
        users = session.nearby_users(limit=1)
        time.sleep(random.randint(3, 15))

    except Exception as e:
        print(e)
        time.sleep(random.randint(3, 15))
        continue

    print("Got user, analyzing.")

    for user in users:
        time.sleep(random.randint(3, 15))
        try:
            photos = user.get_photos()
            images = []
            repeat = False

            for photo in photos:

                file = BytesIO(urlopen(photo).read())
                image = im.open(file)
                images.append(image)
            collage = generate_collage.generate_collage(images)
            collage.save("tmp.jpg")

            results = label_image.use_model("inception_two_class_model.pb", "tmp.jpg")
            os.remove("tmp.jpg")
            choice_type = results[0][0]
            prediction = results[0][1]

            print(user.name, user.age, choice_type, prediction)

            if choice_type == "like" and prediction > 0.5:

                output_name = "automatically_liked/" + str(prediction) + "_" + str(user.name) + "_" + str(user.age) + "_" + str(user.id) + "_collage.jpg"
                # user.like()
                print(output_name)
                collage.save(output_name)
                if prediction >= 0.995:
                    try:
                        print(user.superlike())
                        try:
                            print(user.like())
                        except:
                            pass
                    except:
                        print(user.like())
                else:
                    print(user.like())

            else:
                output_name = "automatically_disliked/" + str(prediction) + "_" + str(user.name) + "_" + str(
                    user.age) + "_" + str(choice_type) + "_"+ str(user.id) + "_collage.jpg"
                # user.dislike()
                print(output_name)
                collage.save(output_name)
                print(user.dislike())

        except Exception as e:
            print(e)
