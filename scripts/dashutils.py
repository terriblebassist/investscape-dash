from scripts import constants
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


def graphformat(title, xtitle, ytitle, height):
    gformat = constants.GRAPH_FORMAT
    gformat['title'] = title
    gformat['xaxis']['title'] = xtitle
    gformat['yaxis']['title'] = ytitle
    gformat['height'] = height
    return gformat


def render_app_layout():
    sidebar = html.Div(
        [
            html.H3("Investscape", className="display-4"),
            html.Hr(),
            html.P(
                "Helps you track your mutual fund investments!",
                className="lead"
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Historical Charts",
                                href="/page-1", id="page-1-link"),
                    dbc.NavLink("Summary", href="/page-2", id="page-2-link"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=constants.SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", style=constants.CONTENT_STYLE)
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


def get_summary_page_layout(x, y1, y2):
    fig = go.Figure(data=[
        go.Bar(
            x=x,
            y=y1,
            name='Invested'),
        go.Bar(
            x=x,
            y=y2,
            name='Current')
    ])
    fig.update_layout(graphformat('Funds Summary', 'Fund',
                                  'Value', 600), barmode='group')
    return html.Div([
        dcc.Graph(id='graph-overall', figure=fig)
    ])


def get_historic_page_layout(dropdowns, funds):
    return html.Div([
        html.Div([
            dcc.Dropdown(id='dropdown', options=dropdowns, value=funds[-1])
        ]),
        dcc.Graph(id='graph-value'),
        dcc.Graph(id='graph-nav'),
        dcc.Graph(id='graph-pl')
    ])
