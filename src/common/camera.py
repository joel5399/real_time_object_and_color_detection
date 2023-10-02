import cv2 as cv


class Camera:
    def __init__(self, cameraDevice):
        self.cameraDevice = cameraDevice

    def openCamera(self):
        self.cam = cv.VideoCapture(self.cameraDevice)
        if not self.cam.isOpened():
            Exception("could not open camera!")

    def readImage(self):
        ret, frame = self.cam.read()
        if not ret:
            return
        return frame

    def closeCamera(self):
        self.cam.release()
