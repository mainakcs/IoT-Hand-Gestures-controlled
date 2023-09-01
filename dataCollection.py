# YouTube Video link - https://www.youtube.com/watch?v=wa2ARoUUdU8

# This python file is used to create the dataset for the project

# In this project first we detect the hands, then we classify the hand sign. It involves both Detection and classification.
# This program is for creating the dataset to train the model for detecting different hand signs


# In this project, firt the webcam captures the image, then that complete image is croped to only the image of hand 
# The hand sign may or may not be symmetric, could have more width than height or vice verse
# But the classifier system needs all the hand signs to be of the same dimensions.
# For that we create a square white box of fixed dimension.
# We place the cropped image of the hand on top of the fixed white square box.
# Then complete image is saved inside the folder. So, all the saved images have the same dimensions even though 
# the particular hand sign could be of unsymmetric in length and width. 


# importing all the dependencies
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector # This library is used for detecting the different hand signs
from matplotlib import image
import numpy as np
import math
import time

# To capture video through the webcam
cap = cv.VideoCapture(0)
detector = HandDetector(maxHands=1)
# maxHand=1 means only one hand is detected at a time, you change the number of hands detected at a time by changing the number (eg. 2 or 3)

offset = 20
imgSize = 300

# Writing the location of the folder where the images of hand signs will be stored
folder = "Data/OFF"
counter = 0

while True: # this while loop is always true, it keeps on looping again and again and keeps detecting the hand continuously
    success, img = cap.read() # reads the captured image and store it in success
    hands, img = detector.findHands(img) # finds the hand in the captured image and stores it in hands variable 
    if hands:
        hand = hands[0]
        x,y,w,h = hand['bbox'] # this gives the dimensions of all the sides of the image and they are stored in x,y,w,h respectively 

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255 # here we create a square of fixed dimensions on top of which the croped image of the hand is put
        imgCrop = img[y-offset : y+h+offset , x-offset : x+w+offset] # here we crop the complete image captured by the camera to fit only the hand

        imgCropShape = imgCrop.shape



        aspectRatio = h/w

        # for puting the image whose height is greater than the width inside the white box
        if aspectRatio >1:
            k = imgSize/h
            wCal = math.ceil(k*w) # the calcuted width to completely fill the white background
            imgResize = cv.resize(imgCrop, (wCal, imgSize)) # resizing the image to the imgSize height and wCal width
            imgResizeShape = imgResize.shape    
            wGap = math.ceil((imgSize-wCal)/2) # the width gap by which the image needs to be shifted
            imgWhite[:, wGap:wCal+wGap] = imgResize # to put the image in the middle of the white background

        # for putting the image whose width is greater than the height in the white box
        else:
            k = imgSize/w
            hCal = math.ceil(k*h)
            imgResize = cv.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape    
            hGap = math.ceil((imgSize-hCal)/2)  
            imgWhite[hGap:hCal + hGap, :] = imgResize        

        cv.imshow("ImageCrop", imgCrop)
        cv.imshow("ImageWhite", imgWhite)


    # code for taking a snap shot of the videostream, this will capture the image of different hand signs
    cv.imshow("Image",img)
    key = cv.waitKey(1)
    if key == ord("s"): # when the 's' key is pressed in the keyboard only then the image is saved inside the specified folder
        counter += 1; # counts the nubmer of images saved
        cv.imwrite(f'{folder}/Image_{time.time()}.jpg',imgWhite) # stores the "imgWhite" image inside the specifed above mentioned folder
        print(counter)