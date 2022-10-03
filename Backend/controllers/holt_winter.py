from collections import OrderedDict
from contextlib import nullcontext
from datetime import datetime
from collections import Counter

#from pandas.io.formats import string
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from dateutil.parser import parse
import numpy as np
import pandas as pd
import time
sheet = nullcontext
data = []


def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


def isContained(candidate, container):
    temp = container
    try:
        for v in candidate:
            temp.remove(v)
        return True
    except ValueError:
        return False


def sort_dict_by_date(the_dict, date_format):
    # Python dicts do not hold their ordering so we need to make it an
    # ordered dict, after sorting.
    return OrderedDict((sorted(
        the_dict.items(),
        key=lambda x: datetime.strptime(x[0], date_format)
    )))


def getOnlyDateAndValue(row):
    rowData = {}
    for i in row.keys():
        if is_date(i):
            rowData.update({i: row[i]})
    return rowData


def calculateSTLOfAllRow(allRowData):
    try:
        start_time = time.time()
        allRowData = getOnlyDateAndValue(allRowData)  # dict of all row
        dataset = np.array(list(allRowData.values()))

        result = ExponentialSmoothing(dataset, trend='add', seasonal='add',
                                      seasonal_periods=12).fit().fittedvalues

        print("--- %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        print(e)


def calculateOutlier():
    try:


        for index, row in enumerate(data):
            kpiAndThresholdValue = {}

            for key in getColumnNameAndValues():
                kpiAndThresholdValue[key] = row[key]
            countZero = Counter(row.values())[0]
            if countZero < 12:
                allRowData = getOnlyDateAndValue(row)  # dict of all row
                dataset = np.array(list(allRowData.values()))

                result = ExponentialSmoothing(dataset, trend='add', seasonal='add',
                                              seasonal_periods=12).fit().fittedvalues


                #stl = STL(np.array(list(allRowData.values())), period=12)
                #result = stl.fit()

                #seasonal, trend, resid  = result.seasonal, result.trend, result.resid
                #estimated = trend + seasonal

        return 1
    except Exception as e:
        print(e)


def getColumnNameAndValues():
    columns = sheet.columns
    uniqueValues = []
    tempCol = {}
    for column in columns:
        if not is_date(column):
            uniqueValue = sheet[column].unique().tolist()
            uniqueValues.append(uniqueValue)
            tempCol[column] = uniqueValue
    return tempCol


def addFile(filePath):
    global sheet
    xls = pd.ExcelFile(filePath)
    sheet = xls.parse(0)  # 2 is the sheet number+1 thus if the file has only 1 sheet write 0 in paranthesis
    sheet["Id"] = sheet.index + 1
    first_column = sheet.pop('Id')
    sheet.insert(0, 'Id', first_column)
    addToData()


def addToData():
    global data
    data = []
    columns = sheet.columns.values
    for rowIndex in range(1, len(sheet)):
        tempCol = {}
        for colIndex in range(0, len(columns)):
            tempCol[columns[colIndex]] = sheet[rowIndex - 1: rowIndex][columns[colIndex]].values[0]
        data.append(tempCol)






