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
from common.image_visualisation import ImageVisualizer

"""
Class description:
The StaticImage class loads an image from the filesystem 
and searches the image for shapes and colors matching the requirements 
from the settings.
"""


class StaticImageApp:
    def __init__(self, pathToImage):
        """
        Constructor
        Create all necessary objects to run application
        :param pathToImage: path to the image as string
        """
        self.pathToImage = pathToImage
        self.imageProcessor = ImageProcessor()
        self.logger = Logger(["Object", "Colora"])
        self.imageReader = ImageReader()
        self.imageVisualizer = ImageVisualizer("imported image")

    def run(self):
        """
        All processes combined and handling of Exceptions
        """
        try:
            image = self.imageReader.readImage(self.pathToImage)
            self.imageProcessor.loadImage(image)
            self.imageProcessor.searchForPatterns()
            self.logger.logDataFromPattern(self.imageProcessor.foundPatterns)
            self.imageVisualizer.displayImgWithPatterns(
                image, self.imageProcessor.foundPatterns
            )
            cv.waitKey()

        except Exception as ex:
            print(f"exception: {ex}")

        finally:
            cv.destroyAllWindows()


if __name__ == "__main__":
    app = StaticImageApp(pathToImage="res/shapes-webcam-picture.jpg")
    app.run()
