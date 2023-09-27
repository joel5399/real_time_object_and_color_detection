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
from common.patterns import Patterns


class ImageProcessor:
    def __init__(self):
        self.originalImage = None

    def loadImage(self, image):
        self.originalImage = image
        self.__preImageProcessing()

    def searchForPatterns(self):
        if self.originalImage is None:
            raise Exception("Load image before searching for patterns!")
        self.__findContours()
        self.__createPatterns()
        self.__handlingDupplicateShapes()

    def __preImageProcessing(self):
        grayImage = cv.cvtColor(self.originalImage, cv.COLOR_BGR2GRAY)

        grayImageBlur = cv.GaussianBlur(grayImage, (9, 9), 0)

        _, self.binaryImage = cv.threshold(
            grayImageBlur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU
        )

        _, self.binaryImage = cv.threshold(grayImageBlur, 125, 255, cv.THRESH_BINARY)

    def __findContours(self):
        self.contours, _ = cv.findContours(
            self.binaryImage, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )
        self.contours = self.contours[1:]

    def __findCorrectShape(self, contour):
        shape = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
        return shape

    def __getCenterOfShape(self, shape):
        moment = cv.moments(shape)
        if moment["m00"] == 0:
            return 0, 0
            # raise Exception("shape has an invalid Moment")

        cx = int(moment["m10"] / moment["m00"])
        cy = int(moment["m01"] / moment["m00"])
        return cx, cy

    def __getColorOfShape(self, cx, cy):
        return self.originalImage[cy, cx]

    def __createPatterns(self):
        self.foundPatterns = []
        for contour in self.contours:
            shape = self.__findCorrectShape(contour)
            cx, cy = self.__getCenterOfShape(shape)
            color = self.__getColorOfShape(cx, cy)
            self.foundPatterns.append(Patterns(len(shape), cx, cy, color))

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

    def printProceedImg(self):
        for patern in self.foundPatterns:
            print(patern)
            """
            cv.circle(
                self.originalImage,
                (patern.centerX, patern.centerY),
                5,
                (127, 127, 127),
                -1,
            )
            """
        cv.drawContours(self.originalImage, self.contours, -1, (0, 255, 0), 3)
        cv.imshow("proceed image", self.originalImage)
        cv.imshow("binary image", self.binaryImage)
