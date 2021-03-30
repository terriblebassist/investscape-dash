MFAPI_URL = 'https://api.mfapi.in/mf/'
MFAPI_DATA = 'data'
MFAPI_DATE = 'date'
MFAPI_NAV = 'nav'
SPREADSHEET_SCOPE = 'https://www.googleapis.com/auth/spreadsheets'
GCREDS_DUMP_FILENAME = 'gcreds.json'
GCREDS_TOKEN_FILENAME = 'token.pickle'
GOOGLE_CREDENTIALS_SERVER = 'GOOGLE_CREDENTIALS'
GOOGLE_CREDENTIALS_LOCAL = 'GOOGLE_CREDENTIALS_JSON'
NAV_MAP_DATE_FORMAT = '%Y-%m-%d'
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE = {
    "margin-left": "25rem",
    "margin-right": "5rem",
    "padding": "2rem 1rem",
}
DATERANGE_SELECTOR = dict(
    buttons=list([
        dict(count=1, label="1M", step="month", stepmode="backward"),
        dict(count=3, label="3M", step="month", stepmode="backward"),
        dict(count=6, label="6M", step="month", stepmode="backward"),
        dict(count=1, label="YTD", step="year", stepmode="todate"),
        dict(count=1, label="1Y", step="year", stepmode="backward"),
        dict(count=3, label="3Y", step="year", stepmode="backward"),
        dict(step="all")
    ])
)
DF_TYPECAST = {
    'value': float,
    'units': float
}
