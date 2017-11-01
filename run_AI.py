from PIL import Image as im
import pynder
from pynder_helpers import get_access_token, get_login_credentials
import generate_collage
from urllib.request import urlopen
from io import BytesIO
import label_image
import os

email, password, FBID = get_login_credentials()
FBTOKEN = get_access_token(email, password)
session = pynder.Session(facebook_id=FBID, facebook_token=FBTOKEN)
print("Session started..")


counter = 1

while True:

    users = []

    try:
        users = session.nearby_users(limit=1)

    except Exception as e:
        print(e)
        continue

    for user in users:

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


                if choice_type == "like":

                    output_name = "automatically_liked/" + str(user.id) + "_" + str(user.name) + "_" + str(user.age) + "_" + str(prediction) + "_collage.jpg"
                    # user.like()
                    print(output_name)
                    # collage.save(output_name)
                    if prediction >= 0.99:
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

                elif choice_type == "dislike":
                    output_name = "automatically_disliked/" + str(user.id) + "_" + str(user.name) + "_" + str(
                        user.age) + "_" + str(prediction) + "_collage.jpg"
                    # user.dislike()
                    print(output_name)
                    # collage.save(output_name)
                    print(user.dislike())


            except Exception as e:
                print(e)
