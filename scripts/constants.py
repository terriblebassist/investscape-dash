from dash_table.Format import Format

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
    "margin-top": "6rem",
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
GRAPH_FORMAT = dict(
        title='title',
        title_x=0.5,
        hovermode="x",
        hoverdistance=100,
        spikedistance=1000,
        legend=dict(
            itemclick="toggleothers",
            itemdoubleclick="toggle",
        ),
        xaxis=dict(
            title='xtitle',
            showspikes=True,
            spikethickness=2,
            spikedash="dot",
            spikecolor="#999999",
            spikemode="across",
            showgrid=False
        ),
        yaxis=dict(
            title='ytitle',
            showgrid=False,
        ),
        template='simple_white',
    )
TABULAR_SUMMARY_VIEW = [
    {'name': 'Scheme', 'id': 'scheme_name'},
    {'name': 'Units', 'id': 'cumunits'},
    {'name': 'Invested', 'id': 'cumsum', 'type': 'numeric',
     'format': Format(group=',')},
    {'name': 'Current', 'id': 'value', 'type': 'numeric',
     'format': Format(group=',')},
    {'name': 'Profit/Loss', 'id': 'pl', 'type': 'numeric',
     'format': Format(group=',')},
    {'name': 'P&L%', 'id': 'plpercent'}
]

TABLE_HEADER_STYLE = {
    'backgroundColor': 'rgb(230, 230, 230)',
    'fontWeight': 'bold',
    'border': '1px solid black'
}
TABLE_CELL_STYLE = {
    'border': '1px solid grey',
    'whiteSpace': 'normal',
    'height': 'auto',
    'textAlign': 'center',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
    'maxWidth': '0'
}
TABLE_CONDITIONAL_STYLE = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    }
]
STYLE_CENTRE_TEXT = {
    'text-align': 'center'
}
TABULAR_TRANSACTION_VIEW = [
    {'name': 'S.No.', 'id': 'serial_no'},
    {'name': 'Date', 'id': 'date'},
    {'name': 'Code', 'id': 'scheme_code'},
    {'name': 'Scheme', 'id': 'scheme_name'},
    {'name': 'Amount', 'id': 'value', 'type': 'numeric',
     'format': Format(group=',')},
    {'name': 'Units', 'id': 'units'},
]
PIE_CHART_CONFIG = dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
)
