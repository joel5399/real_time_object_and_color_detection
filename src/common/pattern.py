import cv2 as cv
import numpy as np

"""
Class description:
The The Pattern class contains the characteristics that defines a pattern.
"""


class Pattern:
    def __init__(
        self, cornerPoints, centerX, centerY, colorBGR, colorTypes, shapeTypes
    ):
        """
        Constructor
        creates a pattern and assign the color and shape as string
        :param cornerPoints: list containing all corner Points of the shape as cv points
        :param centerX: X-coordinate of the shape center point
        :param centerY: Y-coordinate of the shape center point
        :param colorBGR: color in the center of the shape as tuple
        :param colorTypes: color types provided in the pattern properties file
        :param shapeTypes: shape types provided in the pattern properties file
        """
        self.cornerPoints = cornerPoints
        self.centerX = centerX
        self.centerY = centerY
        self.colorString = self.__assignColorClasses(colorBGR, colorTypes)
        self.shapeString = self.__assignShapeClasses(cornerPoints, shapeTypes)

    def __str__(self):
        """
        Get readable string representation of object
        :return: String representation of object
        """
        return f"shape: {self.shapeString}\ncenter: {self.centerX},{self.centerY}\n color: {self.colorString}"

    def __assignColorClasses(self, colorBGR, colorTypes):
        """
        assign BGR to provided colortype
        :param colorBGR: color as tuple
        :param colorTypes: color types provided in the pattern properties file
        :return: color as string if avaible else string "unknown color"
        """
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
        """
        assign shape to provided shapetype
        :param cornerPoints: color as tuple
        :param shapeTypes: shape types provided in the pattern properties file
        :return: shape as string if avaible else string "unknown shape"
        """
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
        """
        compares the smalest and the longest side and compute their ratio
        :param cornerPoints: list containing all corner Points of the shape as cv points
        """
        sides = []
        for i in range(len(cornerPoints)):
            if i != len(cornerPoints) - 1:
                sides.append(np.linalg.norm(cornerPoints[i] - cornerPoints[i + 1]))
            else:
                sides.append(np.linalg.norm(cornerPoints[i] - cornerPoints[0]))

        return max(sides) / min(sides)
