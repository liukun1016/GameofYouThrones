from mysql.mysqldao import select, update
from utility.constant import DB_TB_VIDEO, DB_NAME, TOPIC_USER_VIEW, \
    TOPIC_USER_LIKE, TOPIC_USER_SHARE, TOPIC_USER_SUBSCRIBE, TOPIC_USER_COMMENT
from utility.helper import getTimestampNow, getDateRangeList, generateRandomTimeStr
from kafkaingest.producer import userActivityRandom
from kafkaingest.consumer import flush2Local
from random import randint

def userActivityGenerate(startDate=''):
    videoList = select(DB_NAME, DB_TB_VIDEO, ['id', 'channelid', 'categoryid'],
                        ['useractivityflag'], [{'useractivityflag':'N'}])
    topicRndSeedDict = {
          TOPIC_USER_VIEW:100,
          TOPIC_USER_LIKE:10,
          TOPIC_USER_SHARE:10,
          TOPIC_USER_COMMENT:10,
          TOPIC_USER_SUBSCRIBE:5}
    count = 0
    batchNum = 100
    for video in videoList:
        startDate = "2015-08-01T00:00:00"
        endDate = getTimestampNow()
        for dateValue in getDateRangeList(startDate, endDate, 1):
            dataSet = []
            for topic, value in topicRndSeedDict.items():
                for dateTime in generateRandomTimeStr(dateValue, int(float(randint(0, 2) / 2) * randint(0, value))):
                    dataSet.append(userActivityRandom(topic, vid=video[0], cid=video[1],
                                caid=video[2], dateStr=dateTime))
            flush2Local(batchNum, ''.join(dataSet))
        count = count + 1
        print '----', count
        update(DB_NAME, DB_TB_VIDEO, ['useractivityflag'], ['id'], [{'useractivityflag':'Y', 'id':video[0]}])
        if count > 549:
            break
            batchNum = batchNum + 1
            count = 0
            
#userActivityGenerate()              