import decimal
import json

import pandas as pd
from numpy import outer


def main(file_path: str):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Read in the CSV file
    df = pd.read_csv(file_path, delimiter=";", decimal=",", dtype=object)

    # Filter the datafram to only include ones that have ISIN, Antal and Belopp not equal to -
    df = df[(df['ISIN'] != '-') & (df['Antal'] != '-') & (df['Belopp'] != '-')]

    # Filter the dataframe to only include ones of the desired Typ av transaktion (Köp, Sälj)
    df = df[df['Typ av transaktion'].isin(['Köp', 'Sälj'])]

    # Handle comma separator in Antal and convert to float
    df['Antal'] = pd.to_numeric(
        df['Antal'].str.replace(",", "."), errors='raise')

    # Handle comma separator in Belopp and convert to float
    df['Belopp'] = pd.to_numeric(
        df['Belopp'].str.replace(",", "."), errors='raise')

    # Convert Datum to Date
    df['Datum'] = pd.to_datetime(df['Datum'])

    # Filter the dataframe to only containe dates in may
    # df = df[df['Datum'].dt.month == 5]

    # Filter the datafram to only include transactions of same ISIN that have the same Antal
    df = df.groupby(['ISIN', 'Värdepapper/beskrivning']
                    ).filter(lambda x: x['Antal'].sum() == 0)

    df['Sum buy/sell amount (SEK)'] = df.groupby(['ISIN', 'Typ av transaktion'])[
        'Belopp'].transform('sum')

    df['Gain/loss (SEK)'] = df.groupby('ISIN')['Belopp'].transform('sum')

    df['Gain/loss (%)'] = df['Gain/loss (SEK)'] / \
        (df[df['Sum buy/sell amount (SEK)'] < 0]
         ['Sum buy/sell amount (SEK)'] * -1) * 100

    df['Trade days'] = (df.groupby(['ISIN'])['Datum'].transform('max') -
                        df.groupby(['ISIN'])['Datum'].transform('min')).dt.days

    # Sort dataframe
    df = df.sort_values(by=['Värdepapper/beskrivning',
                        'Datum'], ascending=[True, True])

    output = df.groupby(['Konto', 'ISIN', 'Värdepapper/beskrivning'], as_index=False)[
        ['Konto', 'ISIN', 'Värdepapper/beskrivning', 'Gain/loss (SEK)', 'Gain/loss (%)', 'Trade days']].median()

    if output.empty:
        return json.dumps({'error': 'No data found'})

    return json.dumps({
        'period': f"{df['Datum'].min()} - {df['Datum'].max()}",
        'avg_gain': output[output['Gain/loss (%)'] > 0]['Gain/loss (%)'].mean(),
        'avg_loss': output[output['Gain/loss (%)'] < 0]['Gain/loss (%)'].mean(),
        'win_percentage': (output[output['Gain/loss (%)'] > 0]['Gain/loss (%)'].count() / output['ISIN'].count() * 100) if output['ISIN'].count() else float('nan'),
        'total_trades': int(output['ISIN'].count()),
        'lg_gain': output[output['Gain/loss (%)'] > 0]['Gain/loss (%)'].max(),
        'lg_loss': output[output['Gain/loss (%)'] < 0]['Gain/loss (%)'].min(),
        'avg_gain_days': output[output['Gain/loss (%)'] > 0]['Trade days'].mean(),
        'avg_loss_days': output[output['Gain/loss (%)'] < 0]['Trade days'].mean(),
        'transactions': json.loads(output.to_json(orient='records', lines=False, force_ascii=False))
    })
