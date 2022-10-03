from contextlib import nullcontext
import statistics
from dateutil.parser import parse
import pandas as pd



sheet = nullcontext
data = []


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.
    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


def addToData(sheet):
    global data
    columns = sheet.columns.values
    for rowIndex in range(1, len(sheet)):
        tempCol = {}
        for colIndex in range(0, len(columns)):
            tempCol[columns[colIndex]] = sheet[rowIndex - 1: rowIndex][columns[colIndex]].values[0]
        data.append(tempCol)


def printRow(self):
    global data
    print(data[0])


def getValueOfRow():
    # rowData = []
    rowData = {}
    for i in data[0].keys():
        print(i)
        if is_date(i):
            print(i)
            rowData.update({i: int(data[0][i])})
        # rowData.(int(data[0][i]))
    print(rowData)
    calculateIQR(rowData)
    # calculateMAD(rowData)


def calculateIQR(rowData):
    singleRow = []
    for i in rowData.values():
        singleRow.append(i)
    q3, q1 = np.percentile(singleRow, [75, 25])
    iqr = q3 - q1
    T1 = q1 - 1.5 * iqr
    T3 = q3 + 1.5 * iqr
    print("THis is T3", T3)
    outlier = []
    for i in range(0, len(singleRow)):
        if singleRow[i] > round(T3) or singleRow[i] < round(T1):
            outlier.append(singleRow[i])
    print("This is outlier value", outlier)
    print("row data is", rowData)
    plotValue(rowData, T3)


def plotValue(rowData, T3):
    valueWithDate = rowData.items()
    date, value = zip(*valueWithDate)
    # plt.figure(figsize=(3, 3))
    plt.xticks(rotation=90)
    plt.plot(date, value, lw=2, label='Data')
    plt.axhline(y=T3, color='r', linestyle='--', lw=2, label='Threshold value')
    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
    """fig = plt.figure()
    ax = fig.add_subplot(111)
    x = np.array([1, 3, 5, 3, 1])
    y = np.array([2, 1, 3, 1, 2])
    line, = ax.plot(x, y)

    ymax = T3
    xpos = np.where(y == ymax)
    xmax = x[xpos]"""

    # ax.annotate('local max', xy=(xmax, ymax), xytext=(xmax, ymax + 5), arrowprops=dict(facecolor='black'),)

    # ax.plot(xmax, ymax, 'ro')
    plt.show()


def calculateMAD(rowData):
    median = statistics.median(rowData)
    a = robust.mad(rowData, c=1)
    adm = [abs(a - median) for a in rowData]
    mad = statistics.median(adm)
    x4 = [abs(i - median) / mad for i in rowData]
    constant = 1
    mads = constant * x4
    print("mad2", mads)
    print(x4)
    r = []
    for i in range(0, len(x4)):
        if x4[i] > a:
            r.append(rowData[i])
    print(r)


def getColumnNameAndValues():
    columns = sheet.columns
    uniqueValues = []
    tempCol = {}
    for column in columns:
        if not is_date(column):
            uniqueValue = sheet[column].unique()
            uniqueValues.append(uniqueValue)
            tempCol[column] = uniqueValue
    return tempCol


def abc():
    columns = sheet.columns
    Values = []
    tempCol = {}
    for column in columns:
        if not is_date(column):
            Value = sheet[column]
            Values.append(Value)
            tempCol[column] = Value
    return tempCol


def contained(candidate, container):
    temp = container
    try:
        for v in candidate:
            temp.remove(v)
            #print(temp.index(row))
        return True
    except ValueError:
        return False





def matchFileWithData(singleColumn):
    #print(list(singleColumn.values()))
    for row in data:
        print(list(row.values()))
        print(contained(list(singleColumn.values()), list(row.values())))
        #print(temp.index(row))


def addFile(filePath):
    global sheet
    xls = pd.ExcelFile(filePath)
    sheet = xls.parse(0)  # 2 is the sheet number+1 thus if the file has only 1 sheet write 0 in paranthesis
    addToData(sheet)
    # printRow(sheetX)
    # getValueOfRow()
    # getColumn(sheetX)
    # return getColumn


