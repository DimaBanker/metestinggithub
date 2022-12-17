import pandas as pd

dfm_df = pd.read_csv('dfm_data.csv', sep=';')
ruonia_df = pd.read_csv('ruonia_data.csv', sep=';')

print(dfm_df.head())
print(ruonia_df.head())
