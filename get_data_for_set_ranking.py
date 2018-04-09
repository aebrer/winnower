"""
Will connect to Tinder, and will download all the images of a user, make a collage, and save it. Will run until stopped.
"""


from PIL import Image as im
import pynder
import generate_collage
from urllib.request import urlopen
from io import BytesIO
import time
import random

session = pynder.Session(XAuthToken="d3f82ed5-13af-4dd2-9eed-01f88d78edfe")
print("Session started..")

# keep a cache of already seen profiles, so as to avoid duplicates
try:
    seen_users_file = open("seen_users.txt", "r")
    seen_users = [line.rstrip('\n') for line in seen_users_file]
    seen_users_file.close()
except:
    seen_users = []

counter = 1

# no clear reason to me why this doesn't work, and it's not worth figuring out.
while len(seen_users) <= 2000:

    users = []

    try:
        users = session.nearby_users()

    except Exception as e:
        print(e)
        continue

    for user in users:
        time.sleep(random.randint(3, 15))
        if user.id not in seen_users:
            try:
                photos = user.get_photos()
                images = []
                repeat = False

                photo_num = 1
                for photo in photos:

                    file = BytesIO(urlopen(photo).read())
                    image = im.open(file)
                    output_name_single = "unranked_single/" + str(user.id) + "_" + str(user.name) + "_" + str(
                        user.age) + "_" + str(photo_num) + ".jpg"
                    image.save(output_name_single)
                    images.append(image)
                    photo_num += 1

                with open("seen_users.txt", "a") as seen_users_file:
                    seen_users_file.write(str(user.id) + "\n")
                seen_users.append(user.id)
                print(counter)
                counter += 1

            except Exception as e:
                print(e)
