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


seen_images = []
counter = 1

while counter <= 2000:

    users = []

    try:
        users = session.nearby_users()

    except Exception as e:
        print(e)
        continue

    for user in users:

        try:
            photos = user.get_photos()
            images = []

            for photo in photos:

                if photo not in seen_images:
                    file = BytesIO(urlopen(photo).read())
                    image = im.open(file)
                    images.append(image)

                seen_images.append(photo)

            collage = generate_collage.generate_collage(images)

            output_name = "unranked_sets/" + str(counter) + "_" + str(user.name) + "_" + str(user.age) + "_collage.jpg"
            collage.save(output_name)
            counter += 1

        except Exception as e:
            print(e)
