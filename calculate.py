import json

import pandas as pd
from numpy import outer


def main(file_path: str):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Read in the CSV file
    df = pd.read_csv(file_path, delimiter=";", decimal=",")

    # Filter the datafram to only include ones that have ISIN not equal to -
    df = df[df['ISIN'] != '-']

    # Filter the dataframe to only include ones of the desired Typ av transaktion (Köp, Sälj)
    df = df[df['Typ av transaktion'].isin(['Köp', 'Sälj'])]

    # Convert Antal to int
    df['Antal'] = df['Antal'].astype(int)

    # Convert Belopp to float
    df['Belopp'] = df['Belopp'].astype(float)

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

    df['Gain/loss days'] = (df.groupby(['ISIN'])['Datum'].transform('max') -
                            df.groupby(['ISIN'])['Datum'].transform('min')).dt.days

    # Sort dataframe
    df = df.sort_values(by=['Värdepapper/beskrivning',
                        'Datum'], ascending=[True, True])

    output = df.groupby(['ISIN', 'Värdepapper/beskrivning'], as_index=False)[
        ['ISIN', 'Värdepapper/beskrivning', 'Gain/loss (SEK)', 'Gain/loss (%)', 'Gain/loss days']].median()

    return {
        'accounts': df['Konto'].drop_duplicates().tolist(),
        'period': f"{df['Datum'].min()} - {df['Datum'].max()}",
        'avg_gain': output[output['Gain/loss (%)'] > 0]['Gain/loss (%)'].mean(),
        'avg_loss': output[output['Gain/loss (%)'] < 0]['Gain/loss (%)'].mean(),
        'win_percentage': output[output['Gain/loss (%)'] > 0]['Gain/loss (%)'].count() / output['ISIN'].count() * 100,
        'total_trades': int(output['ISIN'].count()),
        'lg_gain': output[output['Gain/loss (%)'] > 0]['Gain/loss (%)'].max(),
        'lg_loss': output[output['Gain/loss (%)'] < 0]['Gain/loss (%)'].min(),
        'avg_gain_days': output[output['Gain/loss (%)'] > 0]['Gain/loss days'].mean(),
        'avg_loss_days': output[output['Gain/loss (%)'] < 0]['Gain/loss days'].mean(),
        'transactions': json.loads(output.to_json(orient='records', lines=False, force_ascii=False))
    }
