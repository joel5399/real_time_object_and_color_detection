import cv2 as cv
import math
from common.pattern import Pattern
import json

"""
Class description:
The Image Processor class processes an image, 
to find the predefined shapes and colors in it.
"""


class ImageProcessor:
    def __init__(self):
        """
        Constructor
        Initialisation and load predefined pattern data (color and shape).
        """
        self.originalImage = None
        self.__loadPatternData()

    def loadImage(self, image):
        """
        Loads an image and prepares it for further processing.
        :param image: image file as cv.Mat()
        """
        self.originalImage = image
        self.__preImageProcessing()

    def searchForPatterns(self):
        """
        Searches and creates patterns found in image.
        """
        if self.originalImage is None:
            raise Exception("Load image before searching for patterns!")
        self.__findContours()
        self.__createPatterns()
        self.__handlingDupplicateShapes()

    def __loadPatternData(self):
        """
        Load predefined pattern data and split in colors and shapes.
        """
        pathToJasonFile = "./properties/pattern_properties.json"
        jsonData = self.__openJsonFile(pathToJasonFile)
        self.colorData = jsonData["colors"]
        self.shapeData = jsonData["shapes"]

    def __openJsonFile(self, pathToJasonFile):
        """
        Load data from json file and perform corresponding error handling.
        :param: pathToJasonFile: path to json file as str
        """
        try:
            file = open(pathToJasonFile, "r")
            data = json.load(file)
            file.close()
            return data

        except FileNotFoundError:
            print(f"file '{pathToJasonFile}' not found")
        except json.JSONDecodeError:
            print(f"the file'{pathToJasonFile}' has invalid json format")

    def __preImageProcessing(self):
        """
        Genarate grey scale image of original image. Apply gaussian blur
        and generate binary image.
        """
        grayImage = cv.cvtColor(self.originalImage, cv.COLOR_BGR2GRAY)
        grayImageBlur = cv.GaussianBlur(grayImage, (5, 5), 0)
        _, self.binaryImage = cv.threshold(grayImageBlur, 127, 255, cv.THRESH_BINARY)

    def __findContours(self):
        """
        Aplly find contours algorithm on binary image.
        """
        self.contours, _ = cv.findContours(
            self.binaryImage, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE
        )

    def __findCorrectShape(self, contour):
        """
        Find valid contours -> Contour area sufficient.
        :param: contour: List of points of one contour
        :return: shape if shape has a sufficient area else, return none
        """
        shape = cv.approxPolyDP(contour, 0.02 * cv.arcLength(contour, True), True)
        if abs(cv.contourArea(contour) < 200 or not (cv.isContourConvex(shape))):
            return

        return shape

    def __getCenterOfShape(self, shape):
        """
        Callculate the center of gravity of a shape.
        :param: shape: List of points defining a shape
        :return: coordinates of the center of gravity
        """
        moment = cv.moments(shape)
        if moment["m00"] == 0:
            print("shape has an invalid Moment")
            return 0, 0

        cx = int(moment["m10"] / moment["m00"])
        cy = int(moment["m01"] / moment["m00"])
        return cx, cy

    def __getColorOfShape(self, cx, cy):
        """
        Evaluate color of the pixel at the center of gravity
        :param: cx: x-coordinate center of gravity
        :param: cy: y-coordinate center of gravity
        :return: color as tuple
        """
        return self.originalImage[cy, cx]

    def __createPatterns(self):
        """
        Create pattern objects of found contours
        """
        self.foundPatterns = []
        for contour in self.contours:
            shape = self.__findCorrectShape(contour)
            if shape is None:
                continue
            cx, cy = self.__getCenterOfShape(shape)
            color = self.__getColorOfShape(cx, cy)
            self.foundPatterns.append(
                Pattern(
                    shape.reshape(-1, 2), cx, cy, color, self.colorData, self.shapeData
                )
            )

    def __findDupplicateShapes(self):
        """
        Find allmost overlaying (identical) shapes
        :return: List of shapes which can be removed due to dupplication
        """
        toleranceBetweenPatterns = 0.03
        duplicatesToRemove = []
        for firstComparer in range(len(self.foundPatterns)):
            for secondComparer in range(firstComparer + 1, len(self.foundPatterns)):
                if math.isclose(
                    self.foundPatterns[firstComparer].centerX,
                    self.foundPatterns[secondComparer].centerX,
                    rel_tol=toleranceBetweenPatterns,
                ) and math.isclose(
                    self.foundPatterns[firstComparer].centerY,
                    self.foundPatterns[secondComparer].centerY,
                    rel_tol=toleranceBetweenPatterns,
                ):
                    duplicatesToRemove.append(secondComparer)
        return duplicatesToRemove

    def __handlingDupplicateShapes(self):
        """
        Delete one of the dupplicate shapes.
        """
        duplicatesToRemove = self.__findDupplicateShapes()
        for index in reversed(duplicatesToRemove):
            del self.foundPatterns[index]
