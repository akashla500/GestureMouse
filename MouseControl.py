import cv2
import pyautogui as mouse


class MouseControl:

    def __init__(self):
        self.rightClickLock = True
        self.leftClickLock = True
        self.leftDoubleClickLock = True
        self.leftClickHoldLock = True
        self.xPreviousIndex, self.yPreviousIndex = 0, 0
        mouse.FAILSAFE = False

    def leftClick(self):
        mouse.click(button='left')

    def rightClick(self):
        mouse.click(button="right")

    def hover(self, landMarkerList):
        xCurrentIndex, yCurrentIndex = landMarkerList[8][1], landMarkerList[8][2]
        xDifference, yDifference = self.xPreviousIndex - xCurrentIndex, self.yPreviousIndex - yCurrentIndex
        if xDifference > 10 or yDifference > 10 or xDifference < -10 or yDifference < -10:
            yDifference = -yDifference
            if abs(xDifference) <= 10:
                xDifference = 0
            if abs(yDifference) <= 10:
                yDifference = 0
            print(xDifference, yDifference)
            if xDifference > 30 or yDifference > 30:
                xDifference *= 1.5
                yDifference *= 1.5
            print(xDifference, yDifference)
            mouse.move(xDifference, yDifference)
        self.xPreviousIndex, self.yPreviousIndex = xCurrentIndex, yCurrentIndex

    def draw(self, captureImage, landMarkerList):
        xThumbTip, yThumbTip = landMarkerList[4][1], landMarkerList[4][2]
        xMiddleTip, yMiddleTip = landMarkerList[12][1], landMarkerList[12][2]
        cv2.circle(captureImage, (xMiddleTip, yMiddleTip), 7, (0, 0, 255), cv2.FILLED)
        cv2.circle(captureImage, (xThumbTip, yThumbTip), 7, (0, 0, 255), cv2.FILLED)

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
            return
        else:
            self.rightClickLock = True

        if yMiddleTip < yMiddleMidDown and xThumbTip < xIndex:
            if self.leftClickLock:
                self.leftClick()
                self.leftClickLock = False
            return
        else:
            self.leftClickLock = True

        if abs(xThumbTip - xIndex) > 70:
            if self.leftDoubleClickLock:
                self.leftClick()
                self.leftClick()
                self.leftDoubleClickLock = False
            return
        else:
            self.leftDoubleClickLock = True

        if abs(xIndex - xMiddle) > abs(xIndexTip - xMiddleTip):
            xIndexTip, yIndexTip = landMarkerList[8][1], landMarkerList[8][2]
            cv2.circle(captureImage, (xIndexTip, yIndexTip), 10, (0, 255, 0), cv2.FILLED)
            self.hover(landMarkerList)

    def mouseControlMode(self, captureImage, landMarkerList):
        yRing = landMarkerList[13][2]
        yRingTip = landMarkerList[16][2]
        yPinky = landMarkerList[17][2]
        yPinkyTip = landMarkerList[20][2]
        if yRingTip > yRing and yPinkyTip > yPinky:
            self.mouseMode(captureImage, landMarkerList)
