from datetime import datetime
import csv


class Logger:
    def __init__(self, columnNames):
        self.columnNames = ["Time"] + columnNames
        self.logfile = open(
            "./log/logfile_" + self.__getDateTodayTimeNow() + ".csv", "w", newline=""
        )
        self.writer = csv.writer(self.logfile)
        self.__writeLogFile(self.columnNames, firstRow=True)

    def logDataFromPattern(self, patterns):
        for pattern in patterns:
            shape = pattern.shapeString
            color = pattern.colorString
            self.__writeLogFile([shape, color])

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


if __name__ == "__main__":
    columnNames = ["Number", "Object", "Colour"]

    dataframe1 = ["1", "triangle", "red"]
    dataframe2 = ["2", "circle", "yellow"]
    dataframe3 = ["3", "square", "blue"]

    try:
        logger = Logger(columnNames)
        logger.writeLogFile(dataframe1)
        logger.writeLogFile(dataframe2)
        logger.writeLogFile(dataframe3)

    except Exception as ex:
        print(ex)
    finally:
        logger.logfile.close()

    print(f"Logfile closed: {logger.logfile.closed}")
