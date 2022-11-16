import tensorflow as tf
import numpy as np
import os
from tensorflow import keras

model = keras.models.load_model('./static/model.h5')

def prediction(im):
    im_predict = tf.keras.utils.img_to_array(im,dtype='float32')
    im_predict = np.expand_dims(im_predict,axis=0)
    pred = model.predict(im_predict)
    result = ""
    if pred[0][0] > pred[0][1]:
        result = "Su postura de espalda es incorrecta al {}%".format(np.round(pred[0][0]*100,4))
    else:
        result = "Su postura de espalda es correcta al {}%".format(np.round(pred[0][1]*100,4))
    return result