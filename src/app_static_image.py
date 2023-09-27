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
 * @Creator:            Joshua Stutz              
"""

import cv2 as cv
from common.processor import ImageProcessor

if __name__ == "__main__":
    imgSrc = cv.imread("res/shapes-webcam-picture.jpg", cv.IMREAD_COLOR)
    cv.imshow("original image", imgSrc)
    print(cv.__version__)
    try:
        imageProcessor = ImageProcessor()
        imageProcessor.loadImage(imgSrc)
        cv.imshow("binary image", imageProcessor.binaryImage)
        imageProcessor.searchForPatterns()
        imageProcessor.printProceedImg()

    except Exception as ex:
        print(ex)
        print("something was happened!")

    cv.waitKey(0)
