import requests
from datetime import date, timedelta

MFAPI_URL = 'https://api.mfapi.in/mf/'


def getFormattedDate(unformatted_date):
    dt = unformatted_date.split('-')
    return dt[2] + '-' + dt[1] + '-' + dt[0]


def modifyDateToWorkingDay(unformatted_date, navMap):
    dt = unformatted_date.split('-')
    decremented_date = date(int(dt[0]), int(dt[1]), int(dt[2]))
    for x in range(1, 8):
        decremented_date -= timedelta(days=1)
        dateStr = decremented_date.strftime('%Y-%m-%d')
        if navMap.get(dateStr) is not None:
            return dateStr

    return unformatted_date


def getHistoricalNavMap(navList):
    navMap = {}
    for schemeCode in navList:
        url = MFAPI_URL + str(schemeCode)
        res = requests.get(url)
        data = res.json()['data']

        fundMap = {}
        for navRow in data:
            fundMap[getFormattedDate(navRow['date'])] = navRow['nav']

        navMap[schemeCode] = fundMap

    return navMap


def getNavForDate(navMap, schemeCode, navDate):
    navDate = navDate.split(' ')[0]
    navMapForFund = navMap.get(schemeCode)
    if navMapForFund.get(navDate) is None:
        navDate = modifyDateToWorkingDay(navDate, navMapForFund)

    navValue = navMapForFund.get(navDate)
    return float(navValue) if navValue != None else 0.0
