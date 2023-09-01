# This program is for turning "ON" or "OFF" the device based on the hand sign shown by the user

# importing all the dependencies
import subprocess
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier # This library is used for classifying the hand signs
import numpy as np
import math

cap = cv2.VideoCapture(0) # capture video through the Webcam
detector = HandDetector(maxHands=1) # specifying the number of hands to detect
classifier = Classifier("converted_keras/keras_model.h5", "converted_keras/labels.txt") # location of the trained Model

offset = 20
imgSize = 300

folder = "Data/C" 
counter = 0

# enumerating the labels
labels = ["ON","OFF"] # open the labels.txt file to see the different labels

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox'] 

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1: # for when the hand sign's height is larger than the width
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False) # the confidence value of the prediction is saved in prediction variable
            # the index of the hand sign predicted by the system is stored in the index variable 
            print(prediction, index) 

            # turns "OFF" or "ON" the particular device based on the hand sign shown by the user
            if (index == 0):
                subprocess.run(["python","on.py"]) # if index is 
                
            if (index == 1):
                subprocess.run(["python","off.py"])

        else: # for when the hand sign's width is larger than the length
            k = imgSize / w 
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)


       # creates a box that only contains the image of the hand
        cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                      (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x-offset, y-offset),
                      (x + w+offset, y + h+offset), (255, 0, 255), 4)

        # opens two windows, one shows the cropped hand image and the other shows the cropped hand sign on top of the white square box
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)