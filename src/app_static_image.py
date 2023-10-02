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
from common.processor import ImageProcessor
from common.logger import Logger
from common.image_reader import ImageReader


class StaticImageApp:
    def __init__(self, pathToImage):
        self.pathToImage = pathToImage
        self.imageProcessor = ImageProcessor()
        self.logger = Logger(["Object", "Colora"])
        self.imageReader = ImageReader()

    def run(self):
        try:
            image = self.imageReader.readImage(self.pathToImage)
            self.imageProcessor.loadImage(image)
            self.imageProcessor.searchForPatterns()
            self.logger.logDataFromPattern(self.imageProcessor.foundPatterns)
            self.imageProcessor.displayProceedImg()
            cv.waitKey()

        except Exception as ex:
            print(f"exception: {ex}")

        finally:
            cv.destroyAllWindows()


if __name__ == "__main__":
    app = StaticImageApp(pathToImage="res/shapes-webcam-picture.jpg")
    app.run()
