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

if __name__ == "__main__":
    fps = 5
    cap_cam = cv.VideoCapture(0)
    imageProcessor = ImageProcessor()

    while 1:
        try:
            _, frame = cap_cam.read()
            imageProcessor.loadImage(frame)
            imageProcessor.searchForPatterns()
            imageProcessor.displayProceedImg()

        except Exception as ex:
            print(ex)

        c = cv.waitKey(int(1000 / fps))
        if c == "q":
            break
