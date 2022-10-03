from collections import OrderedDict
from contextlib import nullcontext
from datetime import datetime
import time
from collections import Counter

#from pandas.io.formats import string
from statsmodels.tsa.seasonal import STL

from dateutil.parser import parse
import numpy as np
import pandas as pd

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


def calculateSTLById(rowData):
    try:
        #rowData = getOnlyDateAndValue(singleRowData)  # dict of single row
        #print(rowData.values())

        stl = STL(np.array(list(rowData.values())), period=12)
        result = stl.fit()

        seasonal, trend, residual = result.seasonal, result.trend, result.resid

        estimated = trend + seasonal  # predicted model  need to plot this in same graph
        estimatedValue = [round(e, 2) for e in list(estimated)]

        resid_mu = residual.mean()
        resid_dev = residual.std()

        lower_threshold = resid_mu - 3 * resid_dev  # threshold
        upper_threshold = resid_mu + 3 * resid_dev

        outlier = (residual < lower_threshold) | (residual > upper_threshold)

        if lower_threshold < 0:
            lower_threshold = -lower_threshold
        lower_bound_value = []
        upper_bound_value = []
        for i in estimatedValue:
            lower_bound = round((i - lower_threshold), 1)
            if lower_bound < 0:
                lower_bound = 0
            upper_bound = round((i + upper_threshold), 1)
            lower_bound_value.append(lower_bound)
            upper_bound_value.append(upper_bound)

        getOutlierIndex = [i for i, x in enumerate(outlier) if x]  # [37] [12, 57]
        outlierValue = []
        outlierIndex = []
        for i in getOutlierIndex:
            if i > len(outlier) - 13:
                outlierValue.append(list(rowData.items())[i])  # outlier with date and value
                outlierIndex.append(i)

        return {"outlierValue": dict(outlierValue), "outlierIndex": list(outlierIndex),
                "lower_bound": lower_bound_value, "upper_bound": upper_bound_value}
    except Exception as e:
        print(e)


def calculateIQRById(rowData):
    try:
        singleRow = []
        for i in rowData.values():
            singleRow.append(i)
        mean = np.mean(singleRow)
        std = np.std(singleRow)
        outlier = []
        threshold = 3
        upperThreshold = round((3 * std) + mean)

        getOutlierIndex = []
        for i in singleRow:
            z = (i - mean) / std
            if z > threshold:
                outlier.append(i)
                getOutlierIndex.append(singleRow.index(i))

        outlierIndex = []
        outlierValue = []
        for i in getOutlierIndex:
            if i > len(outlier) - 13:
                outlierValue.append(list(rowData.items())[i])  # outlier with date and value
                outlierIndex.append(i)
        return {"estimatedValue": list(outlier), "outlierValue": dict(outlierValue),
                "outlierIndex": list(outlierIndex), "lower_bound": [threshold],
                "upper_bound": [upperThreshold]}
    except Exception as e:
        print(e)


def calculateSTLOfAllRow(allRowData):
    try:
        allRowData = getOnlyDateAndValue(allRowData)  # dict of all row
        stl = STL(np.array(list(allRowData.values())), period=12)
        result = stl.fit()

        seasonal, trend, resid = result.seasonal, result.trend, result.resid
        resid_mu = resid.mean()
        resid_dev = resid.std()

        lower_threshold = resid_mu - 3 * resid_dev  # threshold
        upper_threshold = resid_mu + 3 * resid_dev

        outlier = (resid < lower_threshold) | (resid > upper_threshold)
        getOutlierIndex = [i for i, x in enumerate(outlier) if x]  # [37] [12, 57]
        outlierValue = []
        for i in getOutlierIndex:
            if i > len(outlier) - 13:
                outlierValue.append(list(allRowData.items())[i])  # outlier with date and value
        return len(outlierValue) > 0
    except Exception as e:
        print(e)


def calculateIQROfAllRow(allRowData):
    rowData = getOnlyDateAndValue(allRowData)
    singleRow = []
    for i in rowData.values():
        singleRow.append(i)

    mean = np.mean(singleRow)
    std = np.std(singleRow)
    outlier = []
    threshold = 3

    getOutlierIndex = []
    for i in singleRow:
        z = (i - mean) / std
        if z > threshold:
            outlier.append(i)
            getOutlierIndex.append(singleRow.index(i))
    print(len(getOutlierIndex))
    return len(getOutlierIndex) > 0


def calculateOutlier():
    try:

        start_time = time.time()

        dataToSend = []
        for index, row in enumerate(data):
            kpiAndThresholdValue = {}
            print(row)
            for key in getColumnNameAndValues():
                kpiAndThresholdValue[key] = row[key]
            countZero = Counter(row.values())[0]
            if countZero < 12:
                kpiAndThresholdValue['Outlier'] = calculateSTLOfAllRow(row)
            else:
                kpiAndThresholdValue['Outlier'] = calculateIQROfAllRow(row)
            dataToSend.append(kpiAndThresholdValue)
            data[index] = {**row, **kpiAndThresholdValue}
            print("--- %s seconds ---" % (time.time() - start_time))
        return dataToSend
    except Exception as e:
        print(e)


def matchFileWithData(singleColumn):
    valuesToSend = []
    for row in data:
        if isContained(list(singleColumn.values()), list(row.values())):
            valuesToSend = dict(row.items() ^ singleColumn.items())
            valuesToSend = sort_dict_by_date(valuesToSend, '%b %Y')
            break
    return valuesToSend


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


def getDataById(idToMatch):  # the actual row data from the excel file
    matchedRow = []
    for item in data:
        if str(item['Id']) == str(idToMatch['id']):
            matchedRow = getOnlyDateAndValue(item)
            break
    return matchedRow


def getRowToPlot(idToMatch):  #Calculation
    plotValue = {}
    for item in data:
        if str(item['Id']) == str(idToMatch['id']):
            rowData = getOnlyDateAndValue(item)  # dict of single row
            x = list(rowData.values()).count(0)
            if x > 12:
                plotValue = calculateIQRById(rowData)
            else:
                plotValue = calculateSTLById(rowData)
            break
    return plotValue
