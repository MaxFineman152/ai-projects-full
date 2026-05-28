import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS, verbose=2)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []

    # Join each data folder to the path
    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        if os.path.isdir(folder_path) == False:  # Check if valid folder
            continue

        # Join each data file to path
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            # Read each image
            image = cv2.imread(file_path)
            if image is None:  # Check if valid image
                raise Exception("Image found is not a valid image")
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))  # Resize all images to same
            images.append(image)

            label = int(folder)
            labels.append(label)

    # Array of normalised images and labels
    images = np.array(images) / 255.0
    labels = np.array(labels)

    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([

        tf.keras.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),  # Input layer

        tf.keras.layers.Conv2D(32, (3, 3), 
                               activation="relu"),  # Convolution layer
        tf.keras.layers.BatchNormalization(),  # Reduce internal covariate shift via batch norm
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),  # Pooling layer

        tf.keras.layers.Conv2D(64, (3, 3),  # 2nd Convolution layer
                               activation="relu"),
        tf.keras.layers.BatchNormalization(),  # 2nd Batch norm
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),  # 2nd Pooling

        tf.keras.layers.Flatten(),  # Reshape to prepare for dense layers

        tf.keras.layers.Dense(150, 
                              activation="relu", 
                              kernel_regularizer=tf.keras.regularizers.l2(0.001)),  # Dense layer

        tf.keras.layers.Dropout(0.2),  # Dropout (reduce overfitting)

        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")  # Output layer

    ])
    
    model.compile(optimizer='adam',
                  loss="categorical_crossentropy",
                  metrics=['accuracy']
                  )  # Compile model with stats

    return model


if __name__ == "__main__":
    main()
