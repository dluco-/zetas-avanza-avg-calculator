
import pandas as pd


def main(desired_account: str, file_path: str):
    pd.set_option('display.max_rows', None)

    # Read in the CSV file
    df = pd.read_csv(file_path, delimiter=";", decimal=",")

    # Filter the dataframe to only include the desired account
    df = df[df['Konto'] == desired_account]

    # Filter the datafram to only include ones that have ISIN not equal to -
    df = df[df['ISIN'] != '-']

    # Filter the dataframe to only include ones of the desired Typ av transaktion (Köp, Sälj)
    df = df[df['Typ av transaktion'].isin(['Köp', 'Sälj'])]

    # Convert Antal to int
    df['Antal'] = df['Antal'].astype(int)

    # Convert Belopp to float
    df['Belopp'] = df['Belopp'].astype(float)

    # Filter the datafram to only include transactions of same ISIN that have the same Antal
    df = df.groupby(['ISIN', 'Värdepapper/beskrivning']
                    ).filter(lambda x: x['Antal'].sum() == 0)

    df['Sum buy/sell amount (SEK)'] = df.groupby(['ISIN', 'Typ av transaktion'])[
        'Belopp'].transform('sum')

    df['Gain/loss (SEK)'] = df.groupby('ISIN')['Belopp'].transform('sum')

    df['Gain/loss (%)'] = df['Gain/loss (SEK)'] / \
        (df[df['Sum buy/sell amount (SEK)'] < 0]
         ['Sum buy/sell amount (SEK)'] * -1) * 100

    # Sort dataframe
    df = df.sort_values(by=['Värdepapper/beskrivning',
                        'Datum'], ascending=[True, True])

    output = df.groupby(['ISIN', 'Värdepapper/beskrivning'], as_index=False)[
        ['ISIN', 'Värdepapper/beskrivning', 'Gain/loss (SEK)', 'Gain/loss (%)']].median()

    return {
        'account': desired_account,
        'period': f"{df['Datum'].min()} - {df['Datum'].max()}",
        'profit': output['Gain/loss (SEK)'].sum(),
        'numbers': {
            'gain': output[output['Gain/loss (%)'] > 0]['Gain/loss (%)'].count(),
            'loss': output[output['Gain/loss (%)'] < 0]['Gain/loss (%)'].count(),
        },
        'max': {
            'gain': {
                'percentage': output['Gain/loss (%)'].max(),
                'amount': output['Gain/loss (SEK)'].max(),
            },
            'loss': {
                'percentage': output['Gain/loss (%)'].min(),
                'amount': output['Gain/loss (SEK)'].min(),
            }
        },
        'avg': {
            'gain': output[output['Gain/loss (%)'] > 0]['Gain/loss (%)'].mean(),
            'loss': output[output['Gain/loss (%)'] < 0]['Gain/loss (%)'].mean(),
        },
        # 'transactions': output.to_json(orient='records', lines=False, force_ascii=False)
    }
