import plotly.graph_objects as go
from datetime import date

from dash.dependencies import Input, Output, State
from scripts import (
    dataframeutils, dashutils
)
from scripts.dashapp import app
from scripts.mongoconnect import MongoDriver
from flask_caching import Cache
from decouple import config
# from scripts import connectgooglesheets

server = app.server
cache = Cache(server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
TIMEOUT = config('CACHE_TIMEOUT', default=300)


@cache.memoize(timeout=TIMEOUT)
def get_transactions():
    print("fetching transactions")
    mdb = MongoDriver()
    dump = mdb.fetch_collection_in_dataframe()

    # Google sheets integration
    # dump=connectgooglesheets.get_transactions_dump(config('SPREADSHEET_ID'),
    #                                                  config('RANGE_NAME'))
    return dump


@cache.memoize(timeout=TIMEOUT)
def get_timeseries_df(dump):
    return dataframeutils.populate_df_attributes(dump)


@cache.memoize(timeout=TIMEOUT)
def get_current_stats(df):
    return dataframeutils.extract_stats(df)


app.layout = dashutils.render_app_layout()
dump = get_transactions()
df = get_timeseries_df(dump)
funds = dataframeutils.get_distinct_funds(df)
dropdowns = dataframeutils.get_dropdown_map(funds)
currentVal = get_current_stats(df)


@app.callback(
    [Output("submit-button", "n_clicks"),
     Output('dropdown_fund', 'value'),
     Output('date-picker', 'value'),
     Output('transaction_amount', 'value'),
     Output('transaction_units', 'value'),
     Output("alert-success", "is_open"),
     Output("alert-danger", "is_open")
     ],
    [Input('submit-button', 'n_clicks'),
     State('dropdown_fund', 'value'),
     State('date-picker', 'date'),
     State('transaction_amount', 'value'),
     State('transaction_units', 'value'),
     State("alert-success", "is_open"),
     State("alert-danger", "is_open")]
)
def create_transaction(n_clicks, fund, date_value,
                       amount, units, is_open_success, is_open_danger):

    check_inputs = fund != '' and date_value is not None \
        and amount != '' and units != ''

    if n_clicks and check_inputs:
        tr_date = date.fromisoformat(date_value).strftime('%d/%m/%Y')
        dump = get_transactions()
        df = get_timeseries_df(dump)
        currentVal = get_current_stats(df)
        row = currentVal.loc[currentVal['scheme_name'] == fund]
        scheme_code = row['scheme_code'].item()

        mdb = MongoDriver()
        transaction = {
            "date": tr_date,
            "scheme_code": scheme_code,
            "scheme_name": fund,
            "value": amount,
            "units": units
        }
        mdb.insert_document_in_collection(transaction)
        cache.delete_memoized(get_transactions)
        cache.delete_memoized(get_timeseries_df)
        return 0, '', '', '', '', True, False

    return 0, '', '', '', '', False, True


@app.callback(Output('graph-value', 'figure'),
              [Input('dropdown', 'value')])
def update_figure_graph_value(selected_value):
    dump = get_transactions()
    df = get_timeseries_df(dump)
    frame = df.loc[df['scheme_name'] == selected_value]
    x1, y1 = frame['date'].tolist(), frame['cumsum'].tolist()
    x2, y2 = frame['date'].tolist(), frame['value'].tolist()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, name='INVESTED VALUE'))
    fig.add_trace(go.Scatter(x=x2, y=y2, name='ACTUAL VALUE'))
    fig = dashutils.set_figure_attributes(fig, 'VALUE', 'Date',
                                          'Value (INR)')
    return fig


@app.callback(Output('graph-nav', 'figure'),
              [Input('dropdown', 'value')])
def update_figure_graph_nav(selected_value):
    dump = get_transactions()
    df = get_timeseries_df(dump)
    frame = df.loc[df['scheme_name'] == selected_value]
    x1, y1 = frame['date'].tolist(), frame['historicnav'].tolist()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, name='NAV'))
    fig = dashutils.set_figure_attributes(fig, 'NAV', 'Date',
                                          'NAV (INR)')
    return fig


@app.callback(Output('graph-pl', 'figure'),
              [Input('dropdown', 'value')])
def update_figure_graph_pl(selected_value):
    dump = get_transactions()
    df = get_timeseries_df(dump)
    frame = df.loc[df['scheme_name'] == selected_value]
    frame['color'] = frame.apply(
        lambda x: 'red' if x['pl'] < 0 else 'green', axis=1)
    x3, y3 = frame['date'].tolist(), frame['pl'].tolist()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x3, y=y3, name='NAV', marker_color=frame['color']))
    fig = dashutils.set_figure_attributes(fig, 'PROFIT/LOSS', 'Date',
                                          'Profit/Loss (INR)', 'stack')
    return fig


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        return True, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 6)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    dump = get_transactions()
    df = get_timeseries_df(dump)

    if pathname in ["/", "/page-1"]:
        currentVal = get_current_stats(df)
        return dashutils.get_totals(currentVal)
    elif pathname == "/page-2":
        currentVal = get_current_stats(df)
        return dashutils.get_tabular_summary(currentVal)
    elif pathname == "/page-3":
        funds = dataframeutils.get_distinct_funds(df)
        dropdowns = dataframeutils.get_dropdown_map(funds)
        return dashutils.get_historic_page_layout(dropdowns, funds)
    elif pathname == "/page-4":
        return dashutils.get_transactions_page(dump)
    elif pathname == "/page-5":
        funds = dataframeutils.get_distinct_funds(df)
        dropdowns = dataframeutils.get_dropdown_map(funds)
        return dashutils.get_submission_page(dropdowns)
    return dashutils.get_error_messsage(pathname)


if __name__ == "__main__":
    app.run_server()
