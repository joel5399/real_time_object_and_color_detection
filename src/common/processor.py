"""
 * @Projectname:        REAL_TIME_OBJECT_AND_COLOR_DETECTION
 *
 * @Description:        process an image from filesystem
 *                      
 * @IDE:                VSCode
 * @Language:           python
 * @Interpreter:        Python 3.9.16
 * @Platform            Windows 11 Pro
 *
 * @Creation date:      25.09.2023
 * @Creator:            Joshua Stutz & Joel Flepp           
"""

import cv2 as cv
import math
from common.pattern import Pattern
import json


class ImageProcessor:
    def __init__(self):
        self.originalImage = None
        self.__loadPatternData()

    def loadImage(self, image):
        self.originalImage = image
        self.__preImageProcessing()

    def searchForPatterns(self):
        if self.originalImage is None:
            raise Exception("Load image before searching for patterns!")
        self.__findContours()
        self.__createPatterns()
        self.__handlingDupplicateShapes()

    def __loadPatternData(self):
        pathToJasonFile = "./properties/pattern_properties.json"
        jsonData = self.__openJsonFile(pathToJasonFile)
        self.colorData = jsonData["colors"]
        self.shapeData = jsonData["shapes"]

    def __openJsonFile(self, pathToJasonFile):
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
        grayImage = cv.cvtColor(self.originalImage, cv.COLOR_BGR2GRAY)
        grayImageBlur = cv.GaussianBlur(grayImage, (5, 5), 0)
        _, self.binaryImage = cv.threshold(grayImageBlur, 127, 255, cv.THRESH_BINARY)

    def __findContours(self):
        self.contours, _ = cv.findContours(
            self.binaryImage, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE
        )

    def __findCorrectShape(self, contour):
        shape = cv.approxPolyDP(contour, 0.02 * cv.arcLength(contour, True), True)
        if abs(cv.contourArea(contour) < 200 or not (cv.isContourConvex(shape))):
            return

        return shape

    def __getCenterOfShape(self, shape):
        moment = cv.moments(shape)
        if moment["m00"] == 0:
            print("shape has an invalid Moment")
            return 0, 0

        cx = int(moment["m10"] / moment["m00"])
        cy = int(moment["m01"] / moment["m00"])
        return cx, cy

    def __getColorOfShape(self, cx, cy):
        return self.originalImage[cy, cx]

    def __createPatterns(self):
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
        duplicatesToRemove = self.__findDupplicateShapes()
        for index in reversed(duplicatesToRemove):
            del self.foundPatterns[index]

    def displayProceedImg(self):
        for patern in self.foundPatterns:
            print(patern)
            print("--------------------------")

            cv.drawContours(
                self.originalImage, [patern.cornerPoints], -1, (0, 255, 0), 3
            )
            cv.putText(
                self.originalImage,
                patern.colorString + " " + patern.shapeString,
                (patern.centerX, patern.centerY),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv.LINE_AA,
            )
        cv.imshow("proceed image", self.originalImage)
