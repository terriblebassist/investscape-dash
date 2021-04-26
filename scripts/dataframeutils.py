from scripts import constants, connectgooglesheets, historicalnav
# from scripts.mongoconnect import MongoDriver
import pandas as pd
from decouple import config


def create_cumulative_transaction_series_df(df):
    conversions = constants.DF_TYPECAST
    df = df.astype(conversions)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)

    filled_df = (df.set_index('date')
                 .groupby('scheme_code')
                 .apply(lambda d:
                        d.reindex(pd.date_range(min(df.date),
                                                pd.to_datetime('today'),
                                                freq='D')))
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
    # filled_df.to_csv('time_series.csv')
    return filled_df


def populate_df_attributes():
    dump = connectgooglesheets.get_transactions_dump(config('SPREADSHEET_ID'),
                                                     config('RANGE_NAME'))
    # dump.to_csv('transaction_dump.csv')

    # Uncomment to re-assign `dump` from MongoDB
    # mdb = MongoDriver()
    # dump = mdb.fetch_collection_in_dataframe()
    df = create_cumulative_transaction_series_df(dump)
    df = df[['scheme_code', 'scheme_name', 'date', 'cumsum', 'cumunits']]
    df = df[df['cumsum'] != 0.0]

    navMap = historicalnav.getHistoricalNavMap(df['scheme_code']
                                               .unique()
                                               .tolist())

    df['historicnav'] = df.apply(lambda row: historicalnav.getNavForDate(
        navMap, row['scheme_code'], str(row['date'])), axis=1)
    df['value'] = df.apply(lambda row: float(
        row['cumunits']) * row['historicnav'], axis=1)
    df['pl'] = df.apply(lambda row: float(row['value']) -
                        float(row['cumsum']), axis=1)
    return df, dump


def get_distinct_funds(df):
    return list(df['scheme_name'].unique())


def get_dropdown_map(funds):
    dropdowns = []
    for fund in funds:
        f1 = {}
        f1['label'] = fund
        f1['value'] = fund
        dropdowns.append(f1)
    return dropdowns


def extract_stats(df):
    currentVal = df.loc[df.groupby('scheme_code').date.idxmax()]
    currentVal['plpercent'] = currentVal['pl']*100/currentVal['cumsum']
    customview = ['scheme_name', 'cumunits',
                  'cumsum', 'value', 'pl', 'plpercent']
    currentVal = currentVal[customview].round(2)
    round_cols = ['cumsum', 'value', 'pl']
    currentVal[round_cols] = currentVal[round_cols].round(0)
    return currentVal
