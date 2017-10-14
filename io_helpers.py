from skimage.io import imsave
import os


if not os.path.isdir("data/likes"):
    os.makedirs("data/likes")
if not os.path.isdir("data/dislikes"):
    os.makedirs("data/dislikes")

base_folder = "data"


def save_image(image, name, liked):

    filename = base_folder

    if liked:
        filename += "/likes/"
    else:
        filename += "/dislikes/"

    file_url_list = name.split("/")
    filename += file_url_list[-1]

    print(filename)

    imsave(filename, image)


def save_bio(bio, liked):

    filename = base_folder + "/bios.tsv"

    with open(filename, "a") as bios:
        if liked:
            bios.write(
                " ".join(bio.split()) + "\t" + "1" + "\n"
            )
        else:
            bios.write(
                " ".join(bio.split()) + "\t" + "0" + "\n"
            )


def save_age(age, liked):

    filename = base_folder + "/ages.tsv"

    with open(filename, "a") as ages:
        if liked:
            ages.write(
                str(age) + "\t" + "1" + "\n"
            )
        else:
            ages.write(
                str(age) + "\t" + "0" + "\n"
            )

