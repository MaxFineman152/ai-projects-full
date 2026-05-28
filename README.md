# Traffic Sign Classification

A convolutional neural network that classifies German traffic sign images into 43 categories.

---

## Overview
Images are loaded from a folder structure, resized to 30×30, normalised, and used to train a CNN built with TensorFlow/Keras.

---

## Model
- Conv2D (32) → BatchNorm → MaxPooling  
- Conv2D (64) → BatchNorm → MaxPooling  
- Flatten → Dense (150, L2 regularisation) → Dropout  
- Dense output layer (43 classes, Softmax)

---

## Training
- Epochs: 10  
- Train/test split: 60/40  
- Optimiser: Adam  
- Loss: Categorical crossentropy  

---

## Output
Trained model that predicts one of 43 traffic sign classes from an image.
