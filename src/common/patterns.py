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


class Patterns:
    def __init__(self, cornerPoints, centerX, centerY, color):
        self.cornerPoints = cornerPoints
        self.centerX = centerX
        self.centerY = centerY
        self.color = color

    def __str__(self):
        return f"number of corners: {len(self.cornerPoints)}\ncenter: {self.centerX},{self.centerY}\ncolor: B = {self.color[0]}, G = {self.color[1]}, R = {self.color[2]}"
