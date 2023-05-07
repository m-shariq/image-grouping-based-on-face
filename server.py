import base64
import glob
import os
import shutil
from typing import List

import cv2
import face_recognition
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from matplotlib import pyplot as plt


def get_image_files(directory):
    """Returns a list of all the image files in the given directory"""
    image_files = glob.glob(os.path.join(directory, "*.jpg"))
    image_files.extend(glob.glob(os.path.join(directory, "*.jpeg")))
    image_files.extend(glob.glob(os.path.join(directory, "*.png")))
    return image_files


def get_face_feature_vectors(image_files):
    """Returns a dictionary containing the face feature vectors for each image"""
    face_feature_vectors = {}
    for image_file in image_files:
        img = face_recognition.load_image_file(image_file)
        face_locations = face_recognition.face_locations(img)
        face_feature_vectors[image_file] = face_recognition.face_encodings(img, face_locations)
    return face_feature_vectors


def get_grouped_images(face_feature_vectors):
    """Returns a list of dictionaries containing the grouped images"""
    # Create a list to store the groups of images with matching faces
    groups = []

    # Loop through each image and group its faces with matching faces in other images
    for image, encodings in face_feature_vectors.items():
        for encoding in encodings:
            grouped = False
            for i, group in enumerate(groups):
                if face_recognition.compare_faces([encoding], group['encoding'][0])[0]:
                    group['images'].append(image)
                    grouped = True
            if not grouped:
                new_group = {'images': [image], 'encoding': [encoding]}
                groups.append(new_group)

    return groups


def print_grouped_images(groups):
    """Prints the grouped images"""
    for i, group in enumerate(groups):
        print(f"Group {i + 1}")
        for j, image in enumerate(group['images']):
            print(image)
        print()


def display_grouped_images(groups):
    """Displays the grouped images"""
    for i, group in enumerate(groups):
        print(f"Group {i + 1}")
        for j, image in enumerate(group['images']):
            img = cv2.imread(image)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.imshow(img)
            plt.show()
        print()


def HTML_image(image):
    """Returns the HTML code to display an image"""
    # image with height and width as 500
    # create a div of 500px x 500px and display the image in it
    return f'<div style="width: 250px; height: 250px;"><img src="data:image/png;base64,{image}" width="100%" height="100%"></div>'


app = FastAPI()


# ACCEPT MULTIPLE FILES AND THEN RETURN THE GROUPED IMAGES
@app.post("/process_images/", response_class=HTMLResponse)
async def group_images(files: List[UploadFile] = File(...)):
    """Accepts multiple image files and returns the grouped images"""
    # Create a temporary directory to store the images
    directory = "temp"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the images to the temporary directory
    for file in files:
        image_file = os.path.join(directory, file.filename)
        with open(image_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    image_files = get_image_files(directory)

    # Get the face feature vectors for each image
    face_feature_vectors = get_face_feature_vectors(image_files)

    # Get the grouped images
    groups = get_grouped_images(face_feature_vectors)

    # Print the grouped images
    print_grouped_images(groups)

    #  convert the group images to base 64
    for i, group in enumerate(groups):
        for j, image in enumerate(group['images']):
            group['images'][j] = base64.b64encode(open(image, 'rb').read()).decode('ascii')

    # Create the HTML code to display the grouped images
    # display one group in one row and display all the images in that group in one row with a space of 2px and number the groups

    create_html = ""
    for i, group in enumerate(groups):
        create_html += f"<h2>Group {i + 1}</h2>"
        create_html += f"<div style='display: flex; flex-direction: row;'>"
        for j, image in enumerate(group['images']):
            create_html += HTML_image(image)
        create_html += f"</div><br>"

    # Delete the temporary directory
    shutil.rmtree(directory)
    return HTMLResponse(content=create_html, status_code=200)
