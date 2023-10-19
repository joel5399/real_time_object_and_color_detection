from datetime import datetime
import csv

"""
Class description:
The Image Processor class processes an image, 
to find the predefined shapes and colors in it.
"""


class Logger:
    def __init__(self, columnNames, tolerance=20):
        """
        Constructor
        open csv file and write first row with the names
        :param columnNames: list of names witch will be written at the top of the file.
        :param tolerance: tolerance for comparison between the center points in pixel.

        """
        self.tolerance = tolerance
        self.lastFramePatterns = []
        self.columnNames = ["Time"] + columnNames
        self.logfile = open(
            "./log/logfile_" + self.__getDateTodayTimeNow() + ".csv", "w", newline=""
        )
        self.writer = csv.writer(self.logfile)
        self.__writeLogFile(self.columnNames, firstRow=True)

    def logDataFromPattern(self, patterns):
        """
        checks if the Pattern was already existing in last frame,
        if not, write shape and color in log file.
        :param patterns: all the patterns founded in current frame as list of Pattern
        """
        for pattern in patterns:
            if not self.__PatternAlreadyExists(pattern):
                shape = pattern.shapeString
                color = pattern.colorString
                self.__writeLogFile([shape, color])

        self.__updateLastFramePatterns(patterns)

    def __writeLogFile(self, logData, firstRow=False):
        """
        writes the logdata to the csv-file.
        :param logData: list of stirngs whitch contains data to write
        :param firsRow: boolean to set if you want to write the first line
        """
        if not firstRow:
            logData = [self.__getDateTodayTimeNow()] + logData
        self.__checkLogData(logData)
        self.writer.writerow(logData)

    def __checkLogData(self, logData):
        """
        checks if the list of the data to write has the same size as the firs row
        :param logData: list of stirngs whitch contains data to write
        """
        if len(self.columnNames) != len(logData):
            raise Exception(
                "Size of logdata does not match the amount of data columns!"
            )

    def __getDateTodayTimeNow(self):
        """
        :return: time of hte day seperated with dashes
        """
        return datetime.now().strftime("%b-%d-%Y_%H-%M-%S")

    def __PatternAlreadyExists(self, paternToCheck):
        """
        checks if patern has the same center as one before
        :param paternToCheck: patern witch has to be checked
        :return: true if the patern has te same center as one before
        """
        centerX = paternToCheck.centerX
        centerY = paternToCheck.centerY
        for lastFramePattern in self.lastFramePatterns:
            centerXRange = range(
                lastFramePattern.centerX - self.tolerance,
                lastFramePattern.centerX + self.tolerance,
            )
            centerYRange = range(
                lastFramePattern.centerY - self.tolerance,
                lastFramePattern.centerY + self.tolerance,
            )
            if centerX in centerXRange and centerY in centerYRange:
                return True
        return False

    def __updateLastFramePatterns(self, paterns):
        """
        updates the founded patterns so they can be compared in the next frame
        :param paterns: list of patterns to update
        """
        self.lastFramePatterns = paterns
