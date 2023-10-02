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


class WebcamApp:
    def __init__(self, fps, cameraDevice):
        self.fps = fps
        self.imageProcessor = ImageProcessor()
        self.logger = Logger(["Object\t", "Color\t"])
        self.cam = Camera(cameraDevice)
        self.cam.openCamera()

    def run(self):
        try:
            while True:
                frame = self.cam.readImage()
                if len(frame) == 0:
                    continue

                self.imageProcessor.loadImage(frame)
                self.imageProcessor.searchForPatterns()
                # self.logger.writeLogFile(self.imageProcessor.foundPatterns)
                self.imageProcessor.displayProceedImg()
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
