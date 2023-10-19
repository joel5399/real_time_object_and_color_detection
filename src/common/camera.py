import cv2 as cv

"""
Class description:
The camera class handels the open and close procedure of the camera device.
Further images can be read and stored from the camera.
"""


class Camera:
    def __init__(self, cameraDevice):
        """
        Constructor
        :param: cameraDevice: Number of the camera device
        """
        self.cameraDevice = cameraDevice

    def openCamera(self):
        """
        Open camera device and do corresponding error handling.
        """
        self.cam = cv.VideoCapture(self.cameraDevice)
        if not self.cam.isOpened():
            Exception("could not open camera!")

    def readImage(self):
        """
        Get image from camera.
        :return: frame as cv.Mat()
        """
        ret, frame = self.cam.read()
        if not ret:
            return
        return frame

    def closeCamera(self):
        """
        Close Camera.
        :Note: Alway close the camera after it fullfilled its purpose.
        """
        self.cam.release()
