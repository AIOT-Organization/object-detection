import os
import numpy as np
import matplotlib.image as mpimg
from time import time
import math
from PIL import Image

# Set the folder where images are stored
image_folder = "/media/0C96FA4E96FA3832/image_data_1/"

def process_image(img_path):
    print(f"Processing {img_path}")
    image = Image.open(img_path)
    image = image.resize((80, 60))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)  # Add an extra dimension

    # Extract the action key from the filename
    key = img_path.split('_')[0]  # Assuming filename format 'key_timestamp.jpg'
    label_array = label_from_key(key)

    return image_array, label_array

def label_from_key(key):
    # Define a mapping from key to label
    label_mapping = {'forward': [1, 0, 0, 0, 0], 'left': [0, 1, 0, 0, 0],
                     'right': [0, 0, 1, 0, 0], 'stop': [0, 0, 0, 1, 0], 'reverse': [0, 0, 0, 0, 1]}
    return label_mapping.get(key, [0, 0, 0, 0, 0])  # Default label for unknown keys

def process_images(directory, chunk_size=100):
    print("Starting image processing...")
    file_list = [f for f in os.listdir(directory) if f.endswith(".jpg")]
    num_files = len(file_list)
    num_chunks = math.ceil(num_files / chunk_size)

    for chunk in range(num_chunks):
        train_labels = []
        train_imgs = []

        for filename in file_list[chunk * chunk_size: (chunk + 1) * chunk_size]:
            img_path = os.path.join(directory, filename)
            image_array, label_array = process_image(img_path)
            train_imgs.append(image_array)
            train_labels.append(label_array)

        train_imgs = np.vstack(train_imgs)
        train_labels = np.vstack(train_labels)

        # Save processed data for each chunk
        np.savez(f'processed_data_{chunk}.npz', train_imgs=train_imgs, train_labels=train_labels)

    print("Image processing complete.")

if __name__ == '__main__':
    process_images(image_folder)
