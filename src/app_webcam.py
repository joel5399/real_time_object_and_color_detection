"""
 * @Projectname:        REAL_TIME_OBJECT_AND_COLOR_DETECTION
 *
 * @Description:        process a live webcam stream.
 *                      
 * @IDE:                VSCode
 * @Language:           python
 * @Interpreter:        Python 3.9.16
 * @Platform            Windows 11 Pro
 *
 * @Creation date:      25.09.2023
 * @Creator:            Joshua Stutz              
"""

import cv2 as cv
from common.processor import ImageProcessor
from common.camera import Camera
from common.logger import Logger
from common.image_visualisation import ImageVisualizer

"""
Class description:
The WebcamApp continously loads images from given camera device 
and searches the images for shapes and colors matching the requirements 
from the settings.
"""


class WebcamApp:
    def __init__(self, fps, cameraDevice):
        """
        Constructor
        Create all necessary objects to run application
        :param fps: how many frames per second should be progressed
        :param cameraDevice: id of camera device which should be used as integer
        """
        self.fps = fps
        self.imageProcessor = ImageProcessor()
        self.logger = Logger(["Object", "Colora"])
        self.imageVisualizer = ImageVisualizer("live Cam")
        self.cam = Camera(cameraDevice)
        self.cam.openCamera()

    def run(self):
        """
        All processes combined and handling of Exceptions
        """
        try:
            while True:
                frame = self.cam.readImage()
                if len(frame) == 0:
                    continue

                self.imageProcessor.loadImage(frame)
                self.imageProcessor.searchForPatterns()
                self.logger.logDataFromPattern(self.imageProcessor.foundPatterns)
                self.imageVisualizer.displayImgWithPatterns(
                    frame, self.imageProcessor.foundPatterns
                )
                if cv.waitKey(1000 // self.fps) == ord("q"):
                    break

        except Exception as ex:
            print(f"exception: {ex}")

        finally:
            self.cam.closeCamera()
            cv.destroyAllWindows()


if __name__ == "__main__":
    app = WebcamApp(fps=20, cameraDevice=0)
    app.run()
