import cv2
import pyautogui as mouse
import time


class MouseControl:
    startTime = 0
    currentTime = 0

    def __init__(self):
        self.rightClickLock = True
        self.leftClickLock = True
        self.leftDoubleClickLock = True
        self.leftClickHoldLock = True
        mouse.FAILSAFE = False

    def leftClickHold(self):
        print("click and hold")

    def leftClick(self):
        mouse.click(button='left')

    def rightClick(self):
        mouse.click(button="right")

    def hover(self):
        print("hover")

    def draw(self, captureImage, landMarkerList):
        xThumbTip, yThumbTip = landMarkerList[4][1], landMarkerList[4][2]
        xIndexTip, yIndexTip = landMarkerList[8][1], landMarkerList[8][2]
        xMiddleTip, yMiddleTip = landMarkerList[12][1], landMarkerList[12][2]
        cv2.circle(captureImage, (xMiddleTip, yMiddleTip), 7, (0, 0, 255), cv2.FILLED)
        cv2.circle(captureImage, (xThumbTip, yThumbTip), 7, (0, 0, 255), cv2.FILLED)
        cv2.circle(captureImage, (xIndexTip, yIndexTip), 10, (0, 255, 0), cv2.FILLED)

    def mouseMode(self, captureImage, landMarkerList):
        xThumbTip = landMarkerList[4][1]
        xIndex, xMiddle = landMarkerList[5][1], landMarkerList[9][1]
        xIndexTip, xMiddleTip = landMarkerList[8][1], landMarkerList[12][1]
        yMiddleTip, yMiddleMidDown = landMarkerList[12][2], landMarkerList[10][2]
        self.draw(captureImage, landMarkerList)
        if yMiddleTip > yMiddleMidDown and xThumbTip > xIndex:
            if self.rightClickLock:
                self.rightClick()
                self.rightClickLock = False
        else:
            self.rightClickLock = True

        if yMiddleTip < yMiddleMidDown and xThumbTip < xIndex:
            if self.leftClickLock:
                self.startTime = time.time()
                self.leftClickLock = False
                return
            if abs(self.startTime-time.time()) > 0.9:
                self.leftClickHold()
                self.leftClickHoldLock = False
        elif not self.leftClickLock:
            if abs(self.startTime-time.time()) > 0.9 and self.leftClickHoldLock:
                self.leftClick()
                self.leftClickLock = True
                self.leftClickHoldLock = True

        if abs(xThumbTip - xIndex) > 70:
            if self.leftDoubleClickLock:
                self.leftClick()
                self.leftClick()
                self.leftDoubleClickLock = False
        else:
            self.leftDoubleClickLock = True

        if abs(xIndex - xMiddle) > abs(xIndexTip - xMiddleTip):
            self.hover()

    def mouseControlMode(self, captureImage, landMarkerList):
        yRing = landMarkerList[13][2]
        yRingTip = landMarkerList[16][2]
        yPinky = landMarkerList[17][2]
        yPinkyTip = landMarkerList[20][2]
        if yRingTip > yRing and yPinkyTip > yPinky:
            self.mouseMode(captureImage, landMarkerList)
