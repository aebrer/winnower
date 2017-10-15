import cv2
import sys
import numpy as np
import os
from skimage import io
from scipy import misc
import matplotlib.pyplot as plt
from skimage.transform import resize

img_size = 100
faces_in_image_limit = 1


def extract_faces(img):

    face_cascade = cv2.CascadeClassifier('utils/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('utils/haarcascade_eye.xml')

    imageDataFin = []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        if len(eyes) >= 1:
            im = resize(roi_color, (img_size, img_size))
            imageDataFin.append(im)

    if len(imageDataFin) > faces_in_image_limit:
        return []
    else:
        return imageDataFin


def print_progress(total, current):
    sys.stdout.write('\rProgress: %.1f%%' % ((current / total) * 100))
    sys.stdout.flush()


def folder_count(path):
    return len([name for name in path if not name[0] == "."])


images = []
labels = []
data_path = 'data'

dislikes_folder_path = os.listdir(os.path.join(data_path, 'dislikes'))
likes_folder_path = os.listdir(os.path.join(data_path, 'likes'))


def process_folder(path, like_type):

    folder_number_of_files = folder_count(path)
    files_processed = 0

    for img in path:

        print_progress(folder_number_of_files, files_processed)

        if not img.startswith('.'):

            faces = extract_faces(cv2.imread(os.path.join(data_path, os.path.join(like_type, img))))

            for face in faces:
                images.append(face)
                if like_type == 'likes':
                    labels.append(1)
                else:
                    labels.append(0)

            files_processed += 1

    print("\nProcessing of {} images complete".format(like_type))


print("Processing disliked images")
process_folder(dislikes_folder_path, "dislikes")
print("Processing liked images")
process_folder(likes_folder_path, "likes")

images = np.array(images)
labels = np.array(labels)
print("Image processing complete! Hurray!")

print(images.shape)
print(labels.shape)


def save_file(data, file_path_name):
    print("Saving {}.npy".format(file_path_name))
    np.save(file_path_name, data)


save_file(images, "processed_images")
save_file(labels, "processed_labels")