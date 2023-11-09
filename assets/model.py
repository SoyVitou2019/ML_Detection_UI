

# import gradio as gr
import cv2
import numpy as np
from keras.applications.vgg16 import VGG16
import torchvision.models as models
import pickle
from sklearn import preprocessing

def XG_boosting_prediction(img):
    SIZE = 256 # Resized Image
    # Captures test/validation data and labels into respective lists
    img_resized = cv2.resize(img, (SIZE, SIZE))
    img_cvt = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

    pred_images = []
    pred_images.append(img_cvt)

    # Convert lists to arrays numpy
    pred_images = np.array(pred_images)

    # Normalize pixel values to between 0 and 1
    x_pred = pred_images / 255.0

    # Load feature extraction model (VGG16)
    # VGG16(weights='imagenet', include_top=False, input_shape=(SIZE, SIZE, 3))
    vgg_model = models.vgg16(pretrained = True)
    # Send test data through feature extraction process
    x_pred_features = vgg_model.predict(x_pred)
    x_pred_features = x_pred_features.reshape(x_pred_features.shape[0], -1)

    # Load the XGBoost model
    with open(r"D:\CADT StartUp\Test application\assets\pre-final_add_nice.pkl", "rb") as f:
        loaded_model = pickle.load(f)
    prediction = loaded_model.predict(x_pred_features)
    top = loaded_model.predict_proba(x_pred_features)
    
    # # Open the text file in read mode
    file_path = r"D:\CADT StartUp\Test application\assets\class.txt"
    with open(file_path, 'r') as file:
        file_contents = file.readlines()
    classes = [line.strip() for line in file_contents]
    
    
    lebels = classes
    # Encode labels from text to integers.
    le = preprocessing.LabelEncoder()
    le.fit(lebels)
    dic_result = {}
    for i in range(len(lebels)):
        dic_result[le.inverse_transform([i])[0]] = top[0][i]
    sorted_dic_result = sorted(dic_result.items(), key=lambda x: x[1], reverse=True)
    sorted_dic_result = {k: v for k, v in sorted_dic_result}
    return sorted_dic_result