import cv2 as cv


class ImageReader:
    def __init__(self):
        pass

    def readImage(self, pathToImage):
        image = cv.imread(pathToImage, cv.IMREAD_COLOR)
        if len(image) == 0:
            raise Exception("could not load image!")
        return image
