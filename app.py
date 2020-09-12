import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

from connectgooglesheets import get_transactions_dump
from historicalnav import getHistoricalNavMap, getNavForDate


SPREADSHEET_ID = '1mPoXJ3Pv9EmITjFni3Z4dNe2tk8U3yMM0VmUGD8EEPI'
RANGE_NAME = 'transactions'

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

app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA], suppress_callback_exceptions=True)

def getFormat(title, xtitle, ytitle, height):
    return dict(
        title=title,
        hovermode="x",
        hoverdistance=100,
        spikedistance=1000,
        legend=dict(
            itemclick="toggleothers",
            itemdoubleclick="toggle",
        ),
        xaxis=dict(
            title=xtitle,
            showspikes=True,
            spikethickness=2,
            spikedash="dot",
            spikecolor="#999999",
            spikemode="across",
            showgrid=False
        ),
        yaxis=dict(
            title=ytitle,
            showgrid=False,
        ),
        template='simple_white',
        height=height
    )


def getTimeSeriesDf(df):
    conversions = {
        'value': float,
        'units': float
    }
    df = df.astype(conversions)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)

    filled_df = (df.set_index('date')
                 .groupby('scheme_code')
                 .apply(lambda d: d.reindex(pd.date_range(min(df.date), pd.to_datetime('today'), freq='D')))
                 .drop('scheme_code', axis=1)
                 .reset_index('scheme_code')
                 .fillna(0))

    filled_df['cumsum'] = (filled_df['value']).groupby(
        filled_df['scheme_code']).cumsum()
    filled_df['cumunits'] = (filled_df['units']).groupby(
        filled_df['scheme_code']).cumsum()
    filled_df = filled_df.reset_index()
    filled_df['date'] = filled_df['index']

    filled_df['scheme_name'] = filled_df['scheme_name'].replace(
        to_replace=0, method='ffill')
    filled_df = filled_df.reset_index()
    filled_df.to_csv('time_series.csv')
    return filled_df


############### CONSTRUCT DATA SOURCE FOR DASHBOARD #############

dump = get_transactions_dump(SPREADSHEET_ID, RANGE_NAME)
dump.to_csv('transaction_dump.csv')

df = getTimeSeriesDf(dump)
df = df[['scheme_code', 'scheme_name', 'date', 'cumsum', 'cumunits']]
df = df[df['cumsum'] != 0.0]

navMap = getHistoricalNavMap(df['scheme_code'].unique().tolist())

df['historicnav'] = df.apply(lambda row: getNavForDate(
    navMap, row['scheme_code'], str(row['date'])), axis=1)
df['value'] = df.apply(lambda row: float(
    row['cumunits']) * row['historicnav'], axis=1)
df['pl'] = df.apply(lambda row: float(row['value']) -
                    float(row['cumsum']), axis=1)

funds = list(df['scheme_name'].unique())
fundTuples = list(zip(df['scheme_name'].unique(), df['scheme_code'].unique()))
fundMap = {}

for fund in fundTuples:
    fundMap[fund[0]] = fund[1]

dropdowns = []
for fund in funds:
    f1 = {}
    f1['label'] = fund
    f1['value'] = fund
    dropdowns.append(f1)


currentVal = df.loc[df.groupby('scheme_code').date.idxmax()]
currentVal['plpercent'] = currentVal['pl']*100/currentVal['cumsum']
currentVal = currentVal[['scheme_name', 'cumunits', 'cumsum', 'value', 'pl', 'plpercent']].round(2)

#################################################################


@app.callback(Output('graph-value', 'figure'),
              [Input('dropdown', 'value')])
def update_figure(selected_value):

    frame = df.loc[df['scheme_name'] == selected_value]
    x1, y1 = frame['date'].tolist(), frame['cumsum'].tolist()
    x2, y2 = frame['date'].tolist(), frame['value'].tolist()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, name='INVESTED VALUE'))
    fig.add_trace(go.Scatter(x=x2, y=y2, name='ACTUAL VALUE'))

    fig.update_layout(getFormat('Historic Value', 'DATE', 'VALUE (INR)', 500))
    fig.update_xaxes(
        rangeselector=DATERANGE_SELECTOR
    )

    return fig


@app.callback(Output('graph-nav', 'figure'),
              [Input('dropdown', 'value')])
def update_figure(selected_value):
    nav_data_for_fund = navMap.get(fundMap.get(selected_value))
    x1, y1 = [], []
    for key, value in nav_data_for_fund.items():
        x1.append(key)
        y1.append(value)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, name='NAV'))

    fig.update_layout(getFormat('Historic NAV', 'DATE', 'NAV', 500))
    fig.update_xaxes(
        rangeselector=DATERANGE_SELECTOR
    )
    return fig


@app.callback(Output('graph-pl', 'figure'),
              [Input('dropdown', 'value')])
def update_figure(selected_value):
    frame = df.loc[df['scheme_name'] == selected_value]
    frame['color'] = frame.apply(
        lambda x: 'red' if x['pl'] < 0 else 'green', axis=1)
    x3, y3 = frame['date'].tolist(), frame['pl'].tolist()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x3, y=y3, name='NAV', marker_color=frame['color']))

    fig.update_layout(getFormat('PROFIT/LOSS', 'DATE',
                                'P&L', 500), barmode='stack')
    fig.update_xaxes(
        rangeselector=DATERANGE_SELECTOR
    )
    return fig


sidebar = html.Div(
    [
        html.H3("Investscape", className="display-4"),
        html.Hr(),
        html.P(
            "Helps you track your mutual fund investments!", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Historical Charts", href="/page-1", id="page-1-link"),
                dbc.NavLink("Summary", href="/page-2", id="page-2-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 3)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        return True, False
    return [pathname == f"/page-{i}" for i in range(1, 3)]



@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return html.Div([
            html.Div([
                dcc.Dropdown(id='dropdown', options=dropdowns, value=funds[-1])
            ]),
            dcc.Graph(id='graph-value'),
            dcc.Graph(id='graph-nav'),
            dcc.Graph(id='graph-pl')
        ])
    elif pathname == "/page-2":
        fig = go.Figure(data=[
            go.Bar(x=currentVal['scheme_name'].tolist(), y=currentVal['cumsum'].tolist(), name='Invested'),
            go.Bar(x=currentVal['scheme_name'].tolist(), y=currentVal['value'].tolist(), name='Current')
        ])
        fig.update_layout(getFormat('Funds Summary', 'Fund',
                                    'Value', 600), barmode='group')
        return html.Div([
            dcc.Graph(id='graph-overall', figure=fig)
        ])

    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)
