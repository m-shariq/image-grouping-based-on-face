import glob
import os

import cv2
import face_recognition
from matplotlib import pyplot as plt

# Path to the directory containing all the images
directory = "C:\\Users\\shari\\Desktop\\images"

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

def main():
    """Main function"""
    # Get the image files
    image_files = get_image_files(directory)

    # Get the face feature vectors for each image
    face_feature_vectors = get_face_feature_vectors(image_files)

    # Group the images
    groups = get_grouped_images(face_feature_vectors)

    # Print the grouped images
    print_grouped_images(groups)

    # Display the grouped images
    # display_grouped_images(groups)

if __name__ == "__main__":
    main()
