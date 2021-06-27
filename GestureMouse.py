import cv2
import HandDetector as detector
import MouseControl


def main():
    # start video capture
    captureVideo = cv2.VideoCapture(0)
    handDetector = detector.HandDetector(detectionConfidence=0.8)
    mouseControl = MouseControl.MouseControl()
    while True:
        captureStatus, captureImage = captureVideo.read()
        captureImage = handDetector.findHands(captureImage)
        landMarkerList = handDetector.findPosition(captureImage)
        if len(landMarkerList) > 0:
            mouseControl.mouseControlMode(captureImage, landMarkerList)
        handDetector.showFramePerSecond(captureImage)
        cv2.imshow("Image", captureImage)
        cv2.waitKey(10)


if __name__ == "__main__":
    main()
