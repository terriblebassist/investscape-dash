import requests
from datetime import date, timedelta
from scripts import constants


def getFormattedDate(unformatted_date):
    dt = unformatted_date.split('-')
    return dt[2] + '-' + dt[1] + '-' + dt[0]


def modifyDateToWorkingDay(unformatted_date, navMap):
    dt = unformatted_date.split('-')  # YYYY-MM-DD
    decremented_date = date(int(dt[0]), int(dt[1]), int(dt[2]))
    for x in range(1, 8):
        decremented_date -= timedelta(days=1)
        dateStr = decremented_date.strftime(constants.NAV_MAP_DATE_FORMAT)
        if navMap.get(dateStr) is not None:
            return dateStr

    return unformatted_date


def get_response_json_from_url(url):
    return requests.get(url).json()


def getHistoricalNavMap(navList):
    navMap = {}
    for schemeCode in navList:
        res = get_response_json_from_url(constants.MFAPI_URL + str(schemeCode))
        data = res[constants.MFAPI_DATA]

        fundMap = {}
        for navRow in data:
            formattedDate = getFormattedDate(navRow[constants.MFAPI_DATE])
            fundMap[formattedDate] = navRow[constants.MFAPI_NAV]

        navMap[schemeCode] = fundMap

    return navMap


def getNavForDate(navMap, schemeCode, navDate):
    navDate = navDate.split(' ')[0]  # Split timestamp by whitespace
    navMapForFund = navMap.get(schemeCode)
    if navMapForFund.get(navDate) is None:
        navDate = modifyDateToWorkingDay(navDate, navMapForFund)

    navValue = navMapForFund.get(navDate)
    return float(navValue) if navValue is not None else 0.0
