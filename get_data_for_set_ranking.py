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

try:
    seen_users_file = open("seen_users.txt", "r")
    seen_users = [line.rstrip('\n') for line in seen_users_file]
    seen_users_file.close()
except:
    seen_users = []

seen_users_file = open("seen_users.txt", "a")

counter = 1

while counter <= 2000:

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


                collage = generate_collage.generate_collage(images)

                output_name = "unranked_sets/" + str(user.id) + "_" + str(user.name) + "_" + str(user.age) + "_collage.jpg"
                collage.save(output_name)
                seen_users_file.write(user.id)
                seen_users.append(user.id)
                print(counter)
                counter += 1

            except Exception as e:
                print(e)
