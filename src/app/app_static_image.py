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

import numpy as np
import cv2 as cv

if __name__ == "__main__":

    imgSrc = cv.imread("res/sample_image.JPG")
    cv.imshow("Image source", imgSrc)

    





    cv.waitKey(0)

