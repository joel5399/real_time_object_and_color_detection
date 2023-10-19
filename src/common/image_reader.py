import cv2 as cv

"""
Class description:
The ImageReader class loads an image from the filesystem.
"""


class ImageReader:
    def __init__(self):
        """
        Constructor
        """
        pass

    def readImage(self, pathToImage):
        """
        Read an image from a given path and corresponding error handling.
        :param pathToImage: path to the image as string
        :return: image as cv.Mat
        """
        image = cv.imread(pathToImage, cv.IMREAD_COLOR)
        if len(image) == 0:
            raise Exception("could not load image!")
        return image
