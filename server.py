import base64
import os
import shutil
import sys
from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

sys.path.append('./main')
from main import get_image_files, get_face_feature_vectors, get_grouped_images, print_grouped_images


def HTML_image(image):
    """Returns the HTML code to display an image"""
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
