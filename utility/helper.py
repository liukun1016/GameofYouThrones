
from datetime import date, datetime, timedelta as td
from utility.constant import USER_ACTIVETY_TIME_UNIT

def parseDateTimeMinute(timestamp):
    timestamp = str(timestamp)
    if len(timestamp) < 11:
        return ''
    timestamp = timestamp[0:timestamp.rfind(':')]
    timeUnit = str(USER_ACTIVETY_TIME_UNIT * ((int)(timestamp[timestamp.rfind(':') + 1: \
                                                    len(timestamp) + 1]) / USER_ACTIVETY_TIME_UNIT))
    if len(timeUnit[timeUnit.rfind(':') + 1:len(timeUnit)]) <= 2:
        timeUnit = timeUnit[0:timeUnit.rfind(':')] + '00'
    return timestamp[0:timestamp.rfind(':')] + ':' + timeUnit
    

def parseDateString(dateStr):
    # Should be in the format of "2015-9-15T12:00:02.0Z"
    if len(str(dateStr)) < 11:
        return ''
    year = int(dateStr[0:dateStr.find('-')])
    month = int(dateStr[dateStr.find('-') + 1:dateStr.rfind('-')])
    day = int(dateStr[dateStr.rfind('-') + 1:dateStr.find('T')])
    return date(year, month, day)

def getDateRangeList(dateStr1, dateStr2, offset=7):
    # Return a list of date between two dates, with offset as the range unit 
    date1 = parseDateString(dateStr1)
    date2 = parseDateString(dateStr2)
    if date1 > date2:
        date3 = date1
        date1 = date2
        date2 = date3
    delta = date2 - date1
    dateList = []
    i = 0
    while i < delta.days:
        dateList.append(str(date1 + td(days=i)))
        i = i + offset   
    return dateList

def parseVIdByImageURL(url):
    url = url[0:url.rfind("/")]
    url = url[url.rfind("/") + 1:len(url)]
    return url

def transformListToString(strList):
    # Returns a string that concatenates all objects in a list by comma
    if strList is not None:
        for i in xrange(0, len(strList)):
            strList[i] = strList[i].encode('utf-8')
        return ','.join(strList)
    
def getTimestampNow():
    strTimestamp = str(datetime.now()).replace(' ', 'T')
    return strTimestamp[0:strTimestamp.rfind(".")] + "Z"
