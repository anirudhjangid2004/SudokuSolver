from imageProcess import *
from sudokuSolver import *


pathImage = "Images/5.png"
heightImg = 450
widthImg  = 450
model     = initializePredictionModel()


## Preparing the image
img = cv.imread(pathImage)
img = cv.resize(img, (widthImg, heightImg))
imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
imgThreshold = preProcess(img)

## Finding all contours
imgContours   = img.copy()
imgBigContour = img.copy()
contours, heirarchy = cv.findContours(imgThreshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

## Finding the biggest contour
biggest, maxArea = biggestContour(contours)
if biggest.size != 0:
    biggest = reorder(biggest)
    cv.drawContours(imgBigContour, biggest, -1, (255, 255, 0), 50)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv.warpPerspective(img, matrix, (widthImg, heightImg))
    imgDetectedDigits = imgBlank.copy()
    imgWarpColored = cv.cvtColor(imgWarpColored, cv.COLOR_BGR2GRAY)


    ## SPLIT the sudoku for finding each digit available
    imgSolvedDigits = imgBlank.copy()
    boxes = splitBoxes(imgWarpColored)
    print(boxes)

    ## Taking prediction help from model
    numbers = getPrediction(boxes, model)
    print(numbers)

    imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
    numbers = np.asarray(numbers)
    posArray = np.where(numbers > 0, 0, 1)
    print(posArray)

    ## Find the solution of the board
    board = np.array_split(numbers, 9)
    try:
        solve(board)
    except:
        pass

    flatList = []
    for sublist in board:
        for item in sublist:
            flatList.append(item)
    solvedNumbers = flatList*posArray
    imgSolvedDigits = displayNumbers(imgSolvedDigits, solvedNumbers)

    ## Overlay Solution
    pts2 = np.float32(biggest)    #Preparing points for warping
    pts1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgInvWarpColored = cv.warpPerspective(imgSolvedDigits, matrix, (widthImg, heightImg))
    inv_perspective = cv.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
    imgDetectedDigits = drawGrid(imgDetectedDigits)
    imgSolvedDigits = drawGrid(imgSolvedDigits)


    imageArray = ([img, imgThreshold, imgContours, imgBigContour],
                [imgDetectedDigits, imgSolvedDigits, imgInvWarpColored, inv_perspective])
    stackedImage = stackImages(imageArray, 1)
    cv.imshow('Progress: ', stackedImage)

else:
    print("No Sudoku Found")

cv.waitKey(0)