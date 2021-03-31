import plotly.graph_objects as go

from dash.dependencies import Input, Output
from scripts import (
    dataframeutils, dashutils
)
from scripts.dashapp import app


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
    fig = dashutils.set_figure_attributes(fig, 'Historic Value', 'DATE',
                                          'VALUE (INR)', 500)

    return fig


@app.callback(Output('graph-nav', 'figure'),
              [Input('dropdown', 'value')])
def update_figure_graph_nav(selected_value):
    frame = df.loc[df['scheme_name'] == selected_value]
    x1, y1 = frame['date'].tolist(), frame['historicnav'].tolist()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, name='NAV'))
    fig = dashutils.set_figure_attributes(fig, 'Historic NAV', 'DATE',
                                          'NAV', 500)
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
    fig = dashutils.set_figure_attributes(fig, 'PROFIT/LOSS', 'DATE',
                                          'P&L', 500, 'stack')
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
        return dashutils.get_historic_page_layout(dropdowns, funds)
    elif pathname == "/page-2":
        x = currentVal['scheme_name'].tolist()
        y1 = currentVal['cumsum'].tolist()
        y2 = currentVal['value'].tolist()
        return dashutils.get_summary_page_layout(x, y1, y2)
    return dashutils.get_error_messsage(pathname)


if __name__ == "__main__":
    app.run_server()
