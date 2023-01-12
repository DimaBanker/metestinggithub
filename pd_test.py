import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

dfm_df = pd.read_csv('dfm_data.csv', sep=';', decimal=',')
ruonia_df = pd.read_csv('ruonia_data.csv', sep=';', decimal=',')

dfm_df['date'] = pd.to_datetime(dfm_df['date'], dayfirst=True)
dfm_df['rate'] = pd.to_numeric(dfm_df['rate'].str.replace(',', '.'), errors='coerce')
dfm_df.sort_values(by='date')

dfm_df['rate_x_sum'] = dfm_df['rate'] * dfm_df['sum']
dfm_df['maturity_date'] = pd.to_datetime(dfm_df['date']) + pd.to_timedelta(np.ceil(dfm_df['term']), unit="D")

dfm_d_sum = dfm_df.groupby('date').agg({'sum': ['sum'], 'rate_x_sum': ['sum']})
dfm_d_sum['avg_rate'] = dfm_d_sum['rate_x_sum'] / dfm_d_sum['sum']

ruonia_df['date'] = pd.to_datetime(ruonia_df['date'], dayfirst=True)
ruonia_df['value'] = pd.to_numeric(ruonia_df['value'])
ruonia_df.sort_values(by='date', inplace=True)
ruonia_df = ruonia_df.reset_index(drop=True)

dates_df = pd.date_range(datetime.date(2021, 1, 13), datetime.date(2021, 12, 31), freq='d')
cl = ['Date', 'Ruonia', 'DFM rate']
rates = []

for i in range(len(dates_df)):
    dr = ruonia_df['date'].loc[ruonia_df['date'] <= dates_df[i]].max()
    r = ruonia_df['value'].loc[ruonia_df['date'] == dr]
    dfm_df_alive = dfm_df.loc[(dfm_df['maturity_date'] >= dates_df[i]) & (dfm_df['date'] < dates_df[i])]
    s = dfm_df_alive['sum'].sum()
    sr = dfm_df_alive['rate_x_sum'].sum()
    rates.append([dates_df[i], r.iloc[0], sr / s])

rates_df = pd.DataFrame(rates, columns=cl)
pd.set_option('display.float_format', '{:.2f}'.format)

rates_df['Spread'] = rates_df['DFM rate'] - rates_df['Ruonia']
print(rates_df)

plt.plot(rates_df['Date'], rates_df['Spread'])
plt.show()
