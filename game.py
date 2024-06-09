import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0]
initialTime = 0  # Initialize initialTime variable

while True:
    imgBG = cv2.imread('test_img/BG.png')

    success, img = cap.read()  # Renamed SUCCESS to success

    imgScaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find hands
    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605,435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 2
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 1
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)

                    imgAI = cv2.imread(f'test_img/{randomNumber}.jpg', cv2.IMREAD_UNCHANGED)
                    if imgAI is not None:  # Check if image was loaded successfully
                        if imgAI.shape[2] == 3:  # If imgAI has 3 channels (RGB), add an alpha channel
                            imgAI = cv2.cvtColor(imgAI, cv2.COLOR_RGB2RGBA)
                            imgAI[:, :, 3] = 255  # Set alpha channel to full opacity
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
                    else:
                        print(f"Error: Unable to load image 'test_img/{randomNumber}.jpg'")

                    # Player wins
                    if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                        (playerMove == 3 and randomNumber == 2):
                        scores[0] +=1
                    
                    # AI wins
                    if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3):
                        scores[1] +=1

    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        if imgAI is not None:  # Check if image was loaded successfully before overlaying
            imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410,215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 225, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112,215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 225, 255), 6)

    cv2.imshow('BG', imgBG)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    elif key == ord('q'):  # Press 'q' to stop the game
        break


    