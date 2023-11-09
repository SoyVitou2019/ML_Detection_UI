from __future__ import print_function
import requests
import json
import cv2

def send_request(img_input, url):
    addr = url

    # prepare headers for http request
    content_type = 'text'
    headers = {'content-type': content_type}

    # img = cv2.imread(r"C:\Users\soyvi\OneDrive\Pictures\O.1.jpg")
    img = img_input
    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', img)
    # send http request with image and receive response
    response = requests.post(addr, data=img_encoded.tostring(), headers=headers)

    result = json.loads(response.text)
    return result