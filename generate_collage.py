"""
A script to turn a set of images into a randomly laid out collage. Important in order to train on the whole profile 
at once, rather than one at a time.
"""

from PIL import Image as im


def generate_collage(images):

    row_size = 3
    margin = 3

    width = max(image.size[0] + margin for image in images)*row_size
    height = sum(image.size[1] + margin for image in images)
    collage = im.new(mode='RGB', size=(width, height), color=(0,0,0))

    max_x = 0
    max_y = 0
    offset_x = 0
    offset_y = 0

    for i,image in enumerate(images):
        collage.paste(image, (offset_x, offset_y))

        max_x = max(max_x, (offset_x + image.size[0]))
        max_y = max(max_y, (offset_y + image.size[1]))

        if i % row_size == row_size-1:
            offset_y = max_y + margin
            offset_x = 0
        else:
            offset_x += margin + image.size[0]

    collage = collage.crop((0, 0, max_x, max_y))

    return collage
