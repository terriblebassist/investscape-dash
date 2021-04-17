from scripts import constants
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import dash_table
import pandas as pd


def graphformat(title, xtitle, ytitle):
    gformat = constants.GRAPH_FORMAT
    gformat['title'] = title
    gformat['xaxis']['title'] = xtitle
    gformat['yaxis']['title'] = ytitle
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
                       className="container-lg bg-light mx-auto \
                           shadow-lg border-secondary")
    return html.Div([dcc.Location(id="url"), sidebar, content])


def set_figure_attributes(fig, title, xtitle, ytitle, barmode=''):
    if barmode == '':
        fig.update_layout(graphformat(title, xtitle,
                                      ytitle))
    else:
        fig.update_layout(graphformat(title, xtitle,
                                      ytitle), barmode=barmode)
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
                    html.Div(
                        "SELECT FUND",
                        className="lead text-white text-left",
                    )
                ], xs=12, sm=12, md=3, lg=3, xl=3),
                dbc.Col([
                    html.Div([
                        dcc.Dropdown(id='dropdown', options=dropdowns,
                                        value=funds[-1])
                    ])
                ], xs=12, sm=12, md=9, lg=9, xl=9)
            ]),
        ],
            className="container-fluid bg-dark py-3 shadow \
                rounded border border-dark",
        ),

        html.Div([
            dcc.Graph(id='graph-value'),
        ], className="container-fluid my-3 shadow border border-dark"),
        html.Div([
            dcc.Graph(id='graph-nav'),
        ], className="container-fluid my-3 shadow border border-dark"),
        html.Div([
            dcc.Graph(id='graph-pl')
        ], className="container-fluid my-3 shadow border border-dark"),
    ])


def get_bootstrap_card(var, cardheader, color):
    return dbc.Card([
        dbc.CardHeader(
            cardheader,
            style=constants.STYLE_CENTRE_TEXT,
            className=f"lead font-weight-bold text-white bg-{color}"
        ),
        dbc.CardBody([
            html.H4(
                f"{var:,}",
                className=f"card-text text-{color}"
            ),
        ], style=constants.STYLE_CENTRE_TEXT),
    ],
        color=color,
        outline=True,
        className="rounded-top"
    )


def get_tabular_summary(df):
    x = df['scheme_name'].tolist()
    y1 = df['cumsum'].tolist()
    y2 = df['value'].tolist()
    fig = go.Figure(data=[
        go.Bar(x=x, y=y1, name='Invested'),
        go.Bar(x=x, y=y2, name='Current')
    ])
    fig.update_layout(graphformat('FUNDS', 'Fund',
                                  'Value'), barmode='group')

    pii = px.pie(df, values='cumsum', names='scheme_name',
                 title=f"INVESTED : {int(sum(y1)):,}",
                 labels={'cumsum': 'Amount', 'scheme_name': 'Scheme'},
                 hole=0.2)
    pic = px.pie(df, values='value', names='scheme_name',
                 title=f"CURRENT : {int(sum(y2)):,}",
                 labels={'value': 'Amount', 'scheme_name': 'Scheme'},
                 hole=0.2)

    pii.update_layout(
        legend=constants.PIE_CHART_CONFIG,
        title_x=0.50,
        title_y=0.05
    )
    pic.update_layout(
        legend=constants.PIE_CHART_CONFIG,
        title_x=0.50,
        title_y=0.05
    )

    return html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='graph-overall', figure=fig)
            ], xs=12, sm=12, md=12, lg=12, xl=12)
        ],
            className="container-fluid py-3 shadow border border-dark"
        ),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=pii)
                ],
                className="border py-3 border-dark",
                xs=12, sm=12, md=6, lg=6, xl=6
            ),
            dbc.Col([
                dcc.Graph(figure=pic)
                ],
                className="border py-3 border-dark",
                xs=12, sm=12, md=6, lg=6, xl=6
            ),
        ],
            className="container-fluid my-3 shadow",
        ),
    ])


def get_totals(df):
    totalsum = int(df['cumsum'].sum())
    totalcurr = int(df['value'].sum())
    totalpl = int(totalcurr-totalsum)
    pl = round(totalpl*100/totalsum, 2)

    isprofit = "success" if totalpl > 0 else "danger"

    return html.Div([
        html.Div([
            dbc.CardDeck([
                get_bootstrap_card(totalsum, "INVESTED", "dark"),
                get_bootstrap_card(totalcurr, "CURRENT", "dark"),
                get_bootstrap_card(totalpl, "Profit/Loss", isprofit),
                get_bootstrap_card(pl, "Profit/Loss %", isprofit),
            ]),
        ], className="container-fluid py-3 shadow border border-dark"),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=constants.TABULAR_SUMMARY_VIEW,
                data=df.to_dict('records'),
                style_data_conditional=constants.TABLE_CONDITIONAL_STYLE,
                style_header=constants.TABLE_HEADER_STYLE,
                style_cell=constants.TABLE_CELL_STYLE,
                fixed_rows={'headers': True},
                sort_action="native",
                filter_action='native',
            )
        ], className="container-fluid py-3 my-3 shadow \
            border border border-dark")
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
            fixed_rows={'headers': True},
            sort_action="native",
            filter_action='native',
            page_size=10,
            sort_by=[{'column_id': 'epoch', 'direction': 'desc'}],
        )
    ], className="container-fluid mb-3 shadow \
            border border border-dark")
