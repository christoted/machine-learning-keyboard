import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller, Key

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

# Alphabet
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "backspace"]]

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        if button.text == "backspace":
            cv2.rectangle(img, button.pos, (x + w + 150, y + h), (200, 0, 255), cv2.FILLED)
            cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        else:
            cv2.rectangle(img, button.pos, (x + w, y + h), (200, 0, 255), cv2.FILLED)
            cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3)

    return img
finalText = ""

keyboard = Controller()
# Class Button
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    success, img = cap.read()
    # Find the Hand position
    img = detector.findHands(img)
    lmList, bbokInfo = detector.findPosition(img)

    img = drawAll(img, buttonList)
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x+w and y < lmList[8][1] < y + h:

                if button.text == "backspace":
                    cv2.rectangle(img, button.pos, (x + w + 150, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

                    lenBetweenFinger, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if lenBetweenFinger < 40:
                        finalText = finalText[:-1]
                        keyboard.press(Key.backspace)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3)
                        sleep(0.15)
                else:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3)

                    lenBetweenFinger, _, _ = detector.findDistance(8, 12, img, draw=False)
                    print(lenBetweenFinger)

                    if lenBetweenFinger < 40:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3)
                        finalText += button.text
                        sleep(0.15)

    cv2.rectangle(img, (50, 350), (750, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    # Trigger the Webcam
    cv2.imshow("Image", img)
    cv2.waitKey(1)