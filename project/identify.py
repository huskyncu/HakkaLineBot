import tensorflow as tf
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import h5py
def identify(msgID):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    with h5py.File('keras_model.h5', 'r') as f:
        model = tf.keras.models.load_model(f, compile=False)

    # Load the labels
    class_names = open("labels.txt", "r", encoding='utf-8').readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(f"{msgID}.jpg").convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = image.resize(size, resample=Image.BILINEAR)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:])
    print("Confidence Score:", confidence_score)
    if confidence_score>0.8:
        return str(class_name[2:])
    else:
        return "無法辨識圖片，請再重傳一次"