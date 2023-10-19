from datetime import datetime
import csv


class Logger:
    def __init__(self, columnNames):
        self.tolerance = 10  # +/- pxl tolerance
        self.lastFramePatterns = []
        self.columnNames = ["Time"] + columnNames
        self.logfile = open(
            "./log/logfile_" + self.__getDateTodayTimeNow() + ".csv", "w", newline=""
        )
        self.writer = csv.writer(self.logfile)
        self.__writeLogFile(self.columnNames, firstRow=True)

    def logDataFromPattern(self, patterns):
        for pattern in patterns:
            if not self.__PatternAlreadyExists(pattern):
                shape = pattern.shapeString
                color = pattern.colorString
                self.__writeLogFile([shape, color])

        self.__updateLastFramePatterns(patterns)

    def __writeLogFile(self, logData, firstRow=False):
        if not firstRow:
            logData = [self.__getDateTodayTimeNow()] + logData
        self.__checkLogData(logData)
        self.writer.writerow(logData)

    def __checkLogData(self, logData):
        if len(self.columnNames) != len(logData):
            raise Exception(
                "Size of logdata does not match the amount of data columns!"
            )

    def __getDateTodayTimeNow(self):
        return datetime.now().strftime("%b-%d-%Y_%H-%M-%S")

    def __PatternAlreadyExists(self, paternToCheck):
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
        self.lastFramePatterns = paterns
