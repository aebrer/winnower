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

    return filename


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

def save_master(img_urls, age, bio, liked):

    filename = base_folder + "/masterlist.tsv"

    img_string = ""

    for img_url in img_urls:
        img_string = img_string + img_url + "\t"

    with open(filename, "a") as masterlist:

        if liked:
            masterlist.write(
                "1" + "\t" + str(age) + "\t" + bio + "\t" + img_string + "\t" + "\n"
            )

        else:
            masterlist.write(
                "0" + "\t" + str(age) + "\t" + bio + "\t" + img_string + "\t" + "\n"
            )


