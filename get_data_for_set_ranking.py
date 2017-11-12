"""
Will connect to Tinder, and will download all the images of a user, make a collage, and save it. Will run until stopped.
"""


from PIL import Image as im
import pynder
from pynder_helpers import get_access_token, get_login_credentials
import generate_collage
from urllib.request import urlopen
from io import BytesIO


email, password, FBID = get_login_credentials()
FBTOKEN = get_access_token(email, password)
session = pynder.Session(facebook_id=FBID, facebook_token=FBTOKEN)
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
        if user.id not in seen_users:
            try:
                photos = user.get_photos()
                images = []
                repeat = False

                for photo in photos:

                    file = BytesIO(urlopen(photo).read())
                    image = im.open(file)
                    images.append(image)

                # make collage
                collage = generate_collage.generate_collage(images)

                # save collage
                output_name = "unranked_sets/" + str(user.id) + "_" + str(user.name) + "_" + str(user.age) + "_collage.jpg"
                collage.save(output_name)
                with open("seen_users.txt", "a") as seen_users_file:
                    seen_users_file.write(str(user.id) + "\n")
                seen_users.append(user.id)
                print(counter)
                counter += 1

            except Exception as e:
                print(e)
