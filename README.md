# Face Grouping from Images

This Python script uses the `face_recognition` library and OpenCV to detect and group faces in a directory of images. It uses face recognition to encode faces and then groups the faces with matching encodings together. The script then displays the images grouped by faces in a graphical user interface using the `matplotlib` library.

## Dependencies

- `face_recognition` library: This is a Python library that provides simple face recognition capabilities. It can be installed using pip with the command `pip install face_recognition`.
- `OpenCV` library: This is a computer vision library that provides tools for image and video processing. It can be installed using pip with the command `pip install opencv-python`.
- `matplotlib` library: This is a data visualization library for creating static, animated, and interactive visualizations in Python. It can be installed using pip with the command `pip install matplotlib`.

## Usage

1. Clone or download the code from this repository.
2. Install the required libraries as described in the Dependencies section above.
3. Place the images you want to group in a directory. The directory path should be updated in the `directory` variable in the script.
4. Run the script with `python face_grouping.py`.
5. The script will group the faces in the images and display the grouped images in a graphical user interface.

Note: The script works with JPEG, PNG, and JPG file types. If your images are in a different format, you will need to modify the script accordingly.
