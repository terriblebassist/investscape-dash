from scripts import constants
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import dash_table
import pandas as pd


def graphformat(title, xtitle, ytitle, height):
    gformat = constants.GRAPH_FORMAT
    gformat['title'] = title
    gformat['xaxis']['title'] = xtitle
    gformat['yaxis']['title'] = ytitle
    gformat['height'] = height
    return gformat


def render_app_layout():
    sidebar = dbc.NavbarSimple(
        children=[
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/page-1",
                                id="page-1-link"),
                    dbc.NavLink("Charts", href="/page-2",
                                id="page-2-link"),
                    dbc.NavLink("Historical Charts",
                                href="/page-3", id="page-3-link"),
                    dbc.NavLink("Transactions",
                                href="/page-4", id="page-4-link"),
                ],
                pills=True,
                fill=True,
            ),
        ],
        brand="Investscape",
        brand_href="/",
        color="dark",
        dark=True,
        fluid=True,
        fixed="top",
    )

    content = html.Div(id="page-content", style=constants.CONTENT_STYLE,
                       className="container-lg mx-auto shadow")
    return html.Div([dcc.Location(id="url"), sidebar, content])


def set_figure_attributes(fig, title, xtitle, ytitle, height, barmode=''):
    if barmode == '':
        fig.update_layout(graphformat(title, xtitle,
                                      ytitle, height))
    else:
        fig.update_layout(graphformat(title, xtitle,
                                      ytitle, height), barmode=barmode)
    fig.update_xaxes(
        rangeselector=constants.DATERANGE_SELECTOR
    )
    return fig


def get_error_messsage(pathname):
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


def get_historic_page_layout(dropdowns, funds):
    return html.Div([
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P("SELECT FUND :", className="lead")
                ], width=1, align="center"),
                dbc.Col([
                    dcc.Dropdown(id='dropdown', options=dropdowns,
                                 value=funds[-1])
                ], width=11, align="center")
            ]),
        ], className="container-fluid py-3 shadow"),
        html.Div([
            dcc.Graph(id='graph-value'),
        ], className="container-fluid shadow", style={'margin-top': '2rem'}),
        html.Div([
            dcc.Graph(id='graph-nav'),
        ], className="container-fluid shadow", style={'margin-top': '2rem'}),
        html.Div([
            dcc.Graph(id='graph-pl')
        ], className="container-fluid shadow", style={'margin-top': '2rem'}),
    ])


def get_bootstrap_card(var, cardheader, color):
    return dbc.Card([
                    dbc.CardHeader(
                        cardheader,
                        style=constants.STYLE_CENTRE_TEXT,
                        className='lead'
                    ),
                    dbc.CardBody([
                        html.H4(f"{var:,}", className="card-text"),
                    ], style=constants.STYLE_CENTRE_TEXT),
                    ], color=color, outline=True)


def get_tabular_summary(df):
    x = df['scheme_name'].tolist()
    y1 = df['cumsum'].tolist()
    y2 = df['value'].tolist()
    fig = go.Figure(data=[
        go.Bar(x=x, y=y1, name='Invested'),
        go.Bar(x=x, y=y2, name='Current')
    ])
    fig.update_layout(graphformat('Funds', 'Fund',
                                  'Value', 600), barmode='group')

    pii = px.pie(df, values='cumsum', names='scheme_name',
                 title='Invested', labels={'cumsum': 'Amount'})
    pic = px.pie(df, values='value', names='scheme_name',
                 title='Current', labels={'value': 'Amount'})
    pii.update_layout(title_x=0.5)
    pic.update_layout(title_x=0.5)
    return html.Div([
        html.Div([
            dcc.Graph(id='graph-overall', figure=fig)
        ],
            className="container-fluid py-3 my-3 shadow"
        ),
        html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=pii)
                ]),
                dbc.Col([
                    dcc.Graph(figure=pic)
                ]),
            ])
        ],
            className="container-fluid py-3 my-3 shadow"
        ),
    ])


def get_totals(df):
    totalsum = int(df['cumsum'].sum())
    totalcurr = int(df['value'].sum())
    totalpl = int(totalcurr-totalsum)
    pl = round(totalpl*100/totalsum, 2)

    isprofit = "success" if totalpl > 0 else "danger"

    return html.Div([
        dbc.CardDeck([
            get_bootstrap_card(totalsum, "Invested Value", "dark"),
            get_bootstrap_card(totalcurr, "Current Value", "dark"),
        ]),
        html.Hr(),
        dbc.CardDeck([
            get_bootstrap_card(totalpl, "Profit/Loss", isprofit),
            get_bootstrap_card(pl, "Profit/Loss %", isprofit),
        ]),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=constants.TABULAR_SUMMARY_VIEW,
                data=df.to_dict('records'),
                style_data_conditional=constants.TABLE_CONDITIONAL_STYLE,
                style_header=constants.TABLE_HEADER_STYLE,
                style_cell=constants.TABLE_CELL_STYLE,
                style_table=constants.TABLE_STYLE,
                fixed_rows={'headers': True},
                sort_action="native",
                filter_action='native',
            )
        ], className="container-fluid py-3 my-3 shadow")
    ])


def get_transactions_page(sheet):
    sheet = sheet[['transaction_date', 'scheme_code',
                   'scheme_name', 'value', 'units']]
    sheet['epoch'] = pd.to_datetime(sheet['transaction_date'],
                                    format='%d/%m/%Y')
    sheet['epoch'] = sheet['epoch'].astype('int64')
    sheet['serial_no'] = sheet['epoch'].rank(method='first')
    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=constants.TABULAR_TRANSACTION_VIEW,
            data=sheet.to_dict('records'),
            style_data_conditional=constants.TABLE_CONDITIONAL_STYLE,
            style_header=constants.TABLE_HEADER_STYLE,
            style_cell=constants.TABLE_CELL_STYLE,
            style_table=constants.TABLE_STYLE,
            fixed_rows={'headers': True},
            sort_action="native",
            filter_action='native',
            page_size=13,
            sort_by=[{'column_id': 'epoch', 'direction': 'desc'}],
        )
    ])
