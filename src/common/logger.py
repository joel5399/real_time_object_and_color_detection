from datetime import datetime
import csv

"""
Class description:
The Logger class takes the found patterns
and saves their properties in an csv file.
"""


class Logger:
    def __init__(self, columnNames, tolerance=20):
        """
        Constructor
        open csv file and set title of the columns
        :param columnNames: list of column titles.
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
        checks wether the Pattern already existed in last frame or not,
        if not, the shape and color is written in the log file.
        :param patterns: all the patterns found in the current frame as a list of Patterns
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
        :param logData: list of strings whitch contains the data to log
        :param firsRow: boolean to define wether you want to write the first row or not
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
        :return: current time and date seperated with dashes
        """
        return datetime.now().strftime("%b-%d-%Y_%H-%M-%S")

    def __PatternAlreadyExists(self, patternToCheck):
        """
        checks if pattern has the same center as one before
        :param patternToCheck: pattern witch has to be checked
        :return: true if the pattern has te same center as another one
        """
        centerX = patternToCheck.centerX
        centerY = patternToCheck.centerY
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

    def __updateLastFramePatterns(self, patterns):
        """
        updates the found patterns so they can be compared in the next frame
        :param patterns: list of patterns to update
        """
        self.lastFramePatterns = patterns
