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

counter = 1

while counter == 1:

    users = []

    try:
        print("Getting user and sleeping for some seconds:")
        users = session.matches()

    except Exception as e:
        print(e)
        continue

    print("Got user, analyzing.")

    for match in users:

        if match.user is not None:
            user = match.user
        else:
            continue

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

            output_name = "matches/" + str(choice_type) + "_" + str(prediction) + "_" + str(user.name) + "_" + str(user.age) + "_" + str(user.id) + "_collage.jpg"
            # user.like()
            print(output_name)
            collage.save(output_name)

        except Exception as e:
            print(e)

    counter += 1
