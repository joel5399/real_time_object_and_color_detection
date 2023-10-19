import cv2 as cv


class ImageVisualizer:
    def __init__(self, windowName, lineColor=(0, 255, 0), textColor=(255, 255, 255)):
        self.lineColor = lineColor
        self.textColor = textColor
        self.windowName = windowName

    def displayImgWithPatterns(self, frame, foundedPatterns):
        self.__addContoursToImage(frame, foundedPatterns)
        cv.imshow(self.windowName, frame)

    def __addContoursToImage(self, frame, foundedPatterns):
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
        for pattern in foundedPatterns:
            print("------------------------------")
            print(pattern)
            print("------------------------------")
