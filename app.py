import pandas as pd

DESIRED_ACCOUNT = 'Rocket 🚀'
FILE = 'data/transaktioner_2022-01-01_2022-03-26.csv'

pd.set_option('display.max_rows', None)


def format_kronor(x):
    return '{:,.0f} kr'.format(x)


# Read in the CSV file
df = pd.read_csv(FILE, delimiter=";")

# Filter the dataframe to only include the desired account
df = df[df['Konto'] == DESIRED_ACCOUNT]

# Filter the datafram to only include ones that have ISIN not equal to -
df = df[df['ISIN'] != '-']

# Filter the dataframe to only include transactions in the desired date range
# df = df[df['Datum'].str.contains('2022')]

# Convert Antal to int
df['Antal'] = df['Antal'].astype(int)

# Filter the datafram to only include transactions of same ISIN that have the same Antal
df = df.groupby(['ISIN', 'Värdepapper/beskrivning']
                ).filter(lambda x: x['Antal'].sum() == 0)

group = df.groupby(['ISIN', 'Värdepapper/beskrivning'])

sum_sell = group.apply(lambda x: x[x['Belopp'].gt(0)]['Belopp'].sum())
sum_buy = group.apply(lambda x: x[x['Belopp'].lt(0)]['Belopp'].sum())

# Calculate gain or loss
sum_gain = sum_sell + sum_buy

# Calculate the percentage change between the buy and sell
percentage_change = ((sum_sell / sum_buy * -1) - 1) * 100

# Create a dataframe with the desired columns
output = pd.concat(
    [
        sum_sell.apply(format_kronor),
        sum_buy.apply(format_kronor),
        sum_gain.apply(format_kronor),
        percentage_change.apply('{:,.2f} %'.format),
    ],
    axis=1,
    keys=['Sell (SEK)', 'Buy (SEK)', 'Gain (SEK)', 'Change (%)'])

# Sort output by gain
output = output.sort_values(by=['Gain (SEK)'], ascending=False)

print("### SUMMARY ###\n")

print(f"Account:\t {DESIRED_ACCOUNT}")
print(f"Period:\t\t {df['Datum'].min()} - {df['Datum'].max()}\n")

print(f"Max gain:\t {percentage_change.max():.2f} %")
print(f"Max loss:\t {percentage_change.min():.2f} %\n")

print(
    f"Average gain:\t {percentage_change[percentage_change > 0].mean():.2f} %")
print(
    f"Average loss:\t {percentage_change[percentage_change < 0].mean():.2f} %\n")

print(
    f"No. gain/loss:\t {percentage_change[percentage_change > 0].count()}/{percentage_change[percentage_change < 0].count()}")

# print sum of all gains
print(f"Total gain/loss: {sum_gain.sum():,.0f} kr")

print("\n### RESULTS ###\n")

print(output)
