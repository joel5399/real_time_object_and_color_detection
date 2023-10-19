import cv2 as cv

"""
Class description:
The ImageVisualizer a frame, draw the paterns and 
shows the proceed image on the screen
"""


class ImageVisualizer:
    def __init__(self, windowName, lineColor=(0, 255, 0), textColor=(255, 255, 255)):
        """
        Constructor
        :param windowName: Name displayed on the window
        :param lineColor: Color of the drawn shape lines
        :param textColor: Color of the displayed text
        """
        self.lineColor = lineColor
        self.textColor = textColor
        self.windowName = windowName

    def displayImgWithPatterns(self, frame, foundedPatterns):
        """
        Draw the contours on the frame and display it
        :param frame: current frame to display
        :param foundedPatterns: found patterns in the current frame
        """
        self.__addContoursToImage(frame, foundedPatterns)
        cv.imshow(self.windowName, frame)

    def __addContoursToImage(self, frame, foundedPatterns):
        """
        Draw the contours on the frame and add the corresponding text
        :param frame: current frame to display
        :param foundedPatterns: found patterns in the current frame
        """
        for pattern in foundedPatterns:
            cv.drawContours(frame, [pattern.cornerPoints], -1, self.lineColor, 3)
            textToShow = pattern.colorString + " " + pattern.shapeString
            cv.putText(
                frame,
                textToShow,
                (pattern.centerX, pattern.centerY),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                self.textColor,
                2,
                cv.LINE_AA,
            )

    def printFoundedPatterns(self, foundedPatterns):
        """
        print all the found patterns in the current frame
        :param foundedPatterns: found patterns in the current frame
        """
        for pattern in foundedPatterns:
            print("------------------------------")
            print(pattern)
            print("------------------------------")
