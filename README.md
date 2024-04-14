# Potato_Trinity

 Link to the Web App: https://potatotrinity.streamlit.app/

## Overview
This is a simple image classification web application, using both Streamlit and PyTorch used to detect early stage potato diseases. This project was developed by Harshit Kumar Singh, Abhinav Areliya and Prathum Pandey.

## Description

It is an image classification system that utilizes Convolutional Neural Networks (CNN) to predict the condition of potatoes based on images. The system comprises two main components:

1. **Trinity(trainingmodel).py**: This script is responsible for training the CNN model using a provided dataset. After training, the weights are saved into a file named `potatoweights.pth`.

2. **model.py**: This module serves as the connection between the front-end and the trained deep learning model. It loads the pre-trained weights saved in `potatoweights.pth` and uses them to predict the condition of individual potato images. The predictions are returned as probabilities for each class in a dictionary format.


## Performance

Our model was able to achieve 97.3% accuracy on validation dataset. We used the RESNET9 architecture for image classification tasks. 

## Installation

All the necessary libraries are availbale in the [requirements.txt](https://github.com/Amiiney/cld-app-streamlit/blob/main/requirements.txt) file. You need to clone the repository, install requirements.txt and run streamlit.
 
 ```
 git clone https://github.com/PrathumP/Potato_Trinity
 cd Potato_Trinity
 pip install -r requirements.txt
 streamlit run app.py
 ```
 

## Usage

1. **Training the Model**: To train the model, run `Trinity(trainingmodel).py` with the desired dataset. Ensure that the dataset is structured appropriately for image classification tasks.

2. **Using the Model**: Incorporate `model.py` into your front-end application. This module handles receiving individual potato images from the front end, predicting their condition using the pre-trained weights, and returning the probabilities of each class as a dictionary.

## Notes

- Ensure that the necessary dependencies are installed, including libraries for deep learning (e.g., PyTorch, TensorFlow) and image processing (e.g., PIL).
- Customize the model architecture, hyperparameters, and training process as needed for optimal performance.
- Provide appropriate error handling and input validation in the front-end integration to ensure smooth user experience.
- Update the documentation as needed to reflect any changes or enhancements made to the system.

