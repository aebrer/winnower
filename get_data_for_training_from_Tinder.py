from skimage.io import imread
import skimage.io as io
import pynder
import matplotlib.pyplot as plt
from pynder_helpers import get_access_token, get_login_credentials
from io_helpers import save_image, save_bio, save_age

io.use_plugin('matplotlib', 'imshow')

email, password, FBID = get_login_credentials()
FBTOKEN = get_access_token(email, password)
session = pynder.Session(facebook_id=FBID, facebook_token=FBTOKEN)
print("Session started..")

while True:

    try:
        users = session.nearby_users()

    except Exception as e:
        print(e)
        continue

    for user in users:

        photos = user.get_photos()
        bio = user.bio
        age = user.age
        gender = user.gender

        print("Fetched user photos..")

        try:

            image = imread("null.jpg")
            plt.imshow(image)
            plt.pause(0.001)

            if user.bio != '':
                input_string = "\n" + str(user.gender) + \
                               "\n" + str(user.bio) + \
                               "\n\nEnter to dislike, '.' to like, '...' to skip bio:\n\n"
                ans = input(input_string).lower()

                if ans == "...":
                    break
                elif ans == "l":
                    try:
                        user.like()
                    except:
                        pass
                    save_bio(bio, True)
                elif ans == "d":
                    try:
                        user.dislike()
                    except:
                        pass
                    save_bio(bio, False)
                elif ans == ".":
                    save_bio(bio, True)
                else:
                    save_bio(bio, False)

            for photo in photos:

                image = imread(photo)
                plt.imshow(image)
                plt.pause(0.001)

                input_string = "Write '.' to like, hit return to dislike, '...' to skip:\n\n"
                ans = input(input_string).lower()

                if ans == ".":
                    save_image(image, photo, True)
                    save_age(user.age, True)

                elif ans == "l":
                    try:
                        user.like()
                    except:
                        pass

                    save_image(image, photo, True)
                    save_age(user.age, True)

                elif ans == "d":
                    try:
                        user.dislike()
                    except:
                        pass

                    save_image(image, photo, False)
                    save_age(user.age, False)

                elif ans == "...":
                    break
                else:
                    save_image(image, photo, False)
                    save_age(user.age, False)

            ans = input("Hit enter for next user, 'l' to like, or 'd' to dislike:\n")

            if ans == "l":
                try:
                    user.like()
                except:
                    pass

            elif ans == "d":
                try:
                    user.dislike()
                except:
                    pass

        except Exception as e:

            print("Some kind of error.")
            print(e)
