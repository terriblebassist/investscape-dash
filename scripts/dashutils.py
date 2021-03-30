from scripts import constants
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def graphformat(title, xtitle, ytitle, height):
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
