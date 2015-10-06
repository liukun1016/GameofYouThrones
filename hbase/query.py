from hbdao import scanDataByRowPrefix, getDataByRowKeys
from utility.constant import HB_CHANNEL_PREFIX, HB_VIDEO_PREFIX
from random import randint

def scanVideoByIds(idList=None, topn, useractivity, mode):
    columnQualiferList = ['%s%s' % (useractivity, mode)]
    columnQualiferAccumList = ['%s%s_accum' % (useractivity, mode)]
    Filter = "ColumnPrefixFilter('2015-09-30T')"
    if idList is None or len(idList) == 0:
        rows = tuple(scanDataByRowPrefix(HB_VIDEO_PREFIX, columnQualiferList, Filter=Filter))
        rowsAccum = tuple(scanDataByRowPrefix(HB_VIDEO_PREFIX, columnQualiferAccumList, Filter=Filter))
    else:
        rows = tuple(getDataByRowKeys(idList, columnQualiferList))
        rowsAccum = tuple(getDataByRowKeys(idList, columnQualiferAccumList))

def scanVideoByChannel(channelid, topn, dateRangeList, useractivity, mode):
    columnQualiferList = []
    columnQualiferAccumList = []
    columnQualifer = '%s%s' % (useractivity, mode)
    columnQualiferAccum = '%s%s_accum' % (useractivity, mode)
    for dateStr in dateRangeList:
        columnQualiferList.append(columnQualifer + ":" + dateStr)
        columnQualiferAccumList.append(columnQualiferAccum + ":" + dateStr)
    rows = tuple(scanDataByRowPrefix(HB_CHANNEL_PREFIX + HB_VIDEO_PREFIX , columnQualiferList))
    rowsAccum = tuple(scanDataByRowPrefix(HB_CHANNEL_PREFIX + HB_VIDEO_PREFIX, columnQualiferAccumList))
    rndIndex = randint(0, len(rowsAccum) - int(topn))
    topn = int(topn)
    return (parseHBaseTuple(rows[rndIndex:rndIndex + topn], False, dateRangeList),
            parseHBaseTuple(rowsAccum[rndIndex:rndIndex + topn], True, dateRangeList))
        
def parseHBaseTuple(rows, isAccum, dateRangeList):
    # Return a tuple, where each element is also a tuple, that has values 
    # corresponding to the date range list, i.e. sorted
    dataList = []
    for row in rows:
    # channel_video_UCQNg-4bXbDGS61casEa5LyQ:RNK9rMcQL9c 
    # OrderedDict([('userview_daily:2015-10-01', '35'), ('userview_daily:2015-10-03', '92')])
        dataTupleList = row[1].items()
        # dataTupleList = [('userview_daily:2015-10-01', '35'), ('userview_daily:2015-10-03', '92')]
        indexTuple = 0
        dateValueMap = {dateStr:0 for dateStr in dateRangeList}
        for dateStr in dateRangeList:
            columnDate = dataTupleList[indexTuple][0].split(':')[1]
            if columnDate in dateValueMap:
                dateValueMap[columnDate] = dataTupleList[indexTuple][1]
                indexTuple = indexTuple + 1
                if indexTuple >= len(dataTupleList):
                    break
        dateValueList = [dateValueMap[dateRangeList[0]]]
        for i in xrange(1, len(dateRangeList)):
            value = dateValueMap[dateRangeList[i]]
            if isAccum and value == 0:
                value = dateValueList[i - 1]  
            dateValueList.append(value)
        dataList.append(dateValueList)
    return tuple(dataList)
