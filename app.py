import dash
import dash_auth
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from dash.dependencies import Input, Output

from decouple import config
from scripts import (
    constants, dataframeutils, dashutils
)


app = dash.Dash(
    external_stylesheets=[dbc.themes.MATERIA],
    suppress_callback_exceptions=True
)
auth = dash_auth.BasicAuth(
    app,
    {
        config('ADMIN_USERNAME'): config('ADMIN_PASSWORD')
    }
)
server = app.server
app.layout = dashutils.render_app_layout()

df = dataframeutils.populate_df_attributes()
funds = dataframeutils.get_distinct_funds(df)
dropdowns = dataframeutils.get_dropdown_map(funds)
currentVal = dataframeutils.extract_stats(df)


@app.callback(Output('graph-value', 'figure'),
              [Input('dropdown', 'value')])
def update_figure_graph_value(selected_value):

    frame = df.loc[df['scheme_name'] == selected_value]
    x1, y1 = frame['date'].tolist(), frame['cumsum'].tolist()
    x2, y2 = frame['date'].tolist(), frame['value'].tolist()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, name='INVESTED VALUE'))
    fig.add_trace(go.Scatter(x=x2, y=y2, name='ACTUAL VALUE'))

    fig.update_layout(dashutils.graphformat('Historic Value', 'DATE',
                                            'VALUE (INR)', 500))
    fig.update_xaxes(
        rangeselector=constants.DATERANGE_SELECTOR
    )

    return fig


@app.callback(Output('graph-nav', 'figure'),
              [Input('dropdown', 'value')])
def update_figure_graph_nav(selected_value):
    frame = df.loc[df['scheme_name'] == selected_value]
    x1, y1 = frame['date'].tolist(), frame['historicnav'].tolist()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, name='NAV'))

    fig.update_layout(dashutils.graphformat('Historic NAV', 'DATE',
                                            'NAV', 500))
    fig.update_xaxes(
        rangeselector=constants.DATERANGE_SELECTOR
    )
    return fig


@app.callback(Output('graph-pl', 'figure'),
              [Input('dropdown', 'value')])
def update_figure_graph_pl(selected_value):
    frame = df.loc[df['scheme_name'] == selected_value]
    frame['color'] = frame.apply(
        lambda x: 'red' if x['pl'] < 0 else 'green', axis=1)
    x3, y3 = frame['date'].tolist(), frame['pl'].tolist()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x3, y=y3, name='NAV', marker_color=frame['color']))

    fig.update_layout(dashutils.graphformat('PROFIT/LOSS', 'DATE',
                                            'P&L', 500), barmode='stack')
    fig.update_xaxes(
        rangeselector=constants.DATERANGE_SELECTOR
    )
    return fig


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
            go.Bar(
                x=currentVal['scheme_name'].tolist(),
                y=currentVal['cumsum'].tolist(),
                name='Invested'),
            go.Bar(
                x=currentVal['scheme_name'].tolist(),
                y=currentVal['value'].tolist(),
                name='Current')
        ])
        fig.update_layout(dashutils.graphformat('Funds Summary', 'Fund',
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


if __name__ == "__main__":
    app.run_server()
