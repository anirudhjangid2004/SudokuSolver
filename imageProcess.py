import cv2 as cv
import numpy as np
import tensorflow
from keras.models import load_model


def preProcess(img):
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (11, 11), 1)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)
    return imgThreshold

def getPrediction(boxes, model):
    result = []
    for image in boxes:
        ## Preparing the image
        img = np.asarray(image)
        print(f"{img} Abhi asisiis\n\n\n")
        img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]
        print(f"Ye ahi sss {img.shape}")
        img = cv.resize(img, (28,28))
        print(f"Ye ahi abb sss {img.shape}")
        img = img/255
        img = img.reshape(-1, 28, 28, 1)
        print(f"Ye ahi abb sss {img.shape}")

        ## Getting prediction
        predictions = model.predict(img)
        classIndex = np.argmax(predictions, axis=-1)
        probability = np.amax(predictions)
        print(classIndex, probability)

        ## Save to result
        if probability > 0.8: result.append(classIndex[0])
        else: result.append(0)

    return result

def initializePredictionModel():
    model= load_model("Model.h5")
    return model

##Finding the biggest contour
def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv.contourArea(i)
        if area > 50:
            peri = cv.arcLength(i, True)
            approx = cv.approxPolyDP(i, 0.02*peri, True)
            
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    
    return biggest, max_area


## Reordering the points to apply warp perspective
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsnew = np.zeros((4, 1, 2), dtype = np.int32)
    add = myPoints.sum(1)
    myPointsnew[0] = myPoints[np.argmin(add)]
    myPointsnew[3] = myPoints[np.argmax(add)]

    diff = np.diff(myPoints, axis = 1)
    myPointsnew[1] = myPoints[np.argmin(diff)]
    myPointsnew[2] = myPoints[np.argmax(diff)]

    return myPointsnew


## Spliting the sudoku into many small boxes
def splitBoxes(img):
    rows = np.vsplit(img, 9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9)
        for box in cols:
            boxes.append(box)
    return boxes

## Display the digits on the image
def displayNumbers(img, numbers, color=(0, 255, 0)):
    secW = int(img.shape[1]/9)
    secH = int(img.shape[0]/9)
    for x in range(0, 9):
        for y in range(0, 9):
            if numbers[(y*9)+x] != 0:
                cv.putText(img, str(numbers[(y*9)+x]), (x*secW + int(secW/2) - 10, int((y+0.8)*secH)),
                           cv.FONT_HERSHEY_COMPLEX_SMALL, 2, color, 2, cv.LINE_AA)
                
    return img

## To draw grid on the warp perspective
def drawGrid(img):
    secW = int(img.shape[1]/9)
    secH = int(img.shape[0]/9)
    for i in range(0, 9):
        pt1 = (0, secH*i)
        pt2 = (img.shape[1], secH*i)
        pt3 = (secW*i, 0)
        pt4 = (secW*i, img.shape[0])
        cv.line(img, pt1, pt2, (255, 255, 255), 2)
        cv.line(img, pt3, pt4, (255, 255, 255), 2)
    return img

## Function for stacking the images
def stackImages(imgArray, scale):
    rows = len(imgArray)
    cols = len(imgArray[0])

    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv.cvtColor(imgArray[x][y], cv.COLOR_GRAY2BGR)
    
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])

        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        hor_con = np.concatenate(imgArray)
        ver = hor
    
    return ver
