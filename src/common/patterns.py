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
import numpy as np


class Patterns:
    def __init__(
        self, cornerPoints, centerX, centerY, colorBGR, colorTypes, shapeTypes
    ):
        self.cornerPoints = cornerPoints
        self.centerX = centerX
        self.centerY = centerY
        self.colorString = self.__assignColorClasses(colorBGR, colorTypes)
        self.shapeString = self.__assignShapeClasses(cornerPoints, shapeTypes)

    def __str__(self):
        return f"shape: {self.shapeString}\ncenter: {self.centerX},{self.centerY}\n color: {self.colorString}"

    def __assignColorClasses(self, colorBGR, colorTypes):
        if colorTypes is None:
            raise Exception("No possible collors")

        ranges = []
        for colors in colorTypes:
            ranges.append([colors["name"], colors["hsvRange1"]])
            if "hsvRange2" in colors:
                ranges.append([colors["name"], colors["hsvRange2"]])

        colorHsvHue = cv.cvtColor(np.uint8([[colorBGR]]), cv.COLOR_BGR2HSV)[0][0][0]
        for colorName, hsvRange in ranges:
            if hsvRange[0] <= colorHsvHue <= hsvRange[1]:
                return colorName

        return "unknown color"

    def __assignShapeClasses(self, cornerPoints, shapeTypes):
        if shapeTypes is None:
            raise Exception("No possible shapes")

        numberOfCorner = len(cornerPoints)

        shapes = []
        for shape in shapeTypes:
            shapes.append([shape["name"], shape["cornerCount"], shape["edgeRatio"]])

        sideRatio = self.__getSideRatio(cornerPoints)

        for shapeName, cornerCountRange, edgeRatio in shapes:
            if cornerCountRange[0] <= numberOfCorner <= cornerCountRange[1]:
                if edgeRatio != [0]:
                    if edgeRatio[0] <= sideRatio <= edgeRatio[1]:
                        return shapeName
                else:
                    return shapeName

        return "unknown shape"

    def __getSideRatio(self, cornerPoints):
        sides = []
        for i in range(len(cornerPoints)):
            if i != len(cornerPoints) - 1:
                sides.append(np.linalg.norm(cornerPoints[i] - cornerPoints[i + 1]))
            else:
                sides.append(np.linalg.norm(cornerPoints[i] - cornerPoints[0]))

        return max(sides) / min(sides)
