#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

#%%

df = pd.read_csv('BTC-USD-INV.csv')
#%%
df = df.drop(columns=['Open', 'High', 'Low', 'Vol.', 'Change %'])
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].astype(str).str[:10]
df_post_date = df[df['Date'] >= '2016-06-01']
df_post_date['Date'] = pd.Series([dt.datetime.strptime(d, '%Y-%m-%d').date() for d in df_post_date['Date']])
df_post_date = df_post_date[::-1]
#%%
def bought_each_day(row):
    return row['Daily Deposit'] / float(row['Price'].replace(',',''))

def dollars_each_day(row):
    return float(row['Cumulative Buy']) * float(row['Price'].replace(',',''))

df_post_date['Daily Deposit'] = 5.0

df_post_date['Cumulative Deposit'] = df_post_date['Daily Deposit'].cumsum(axis=0)

df_post_date['Daily Buy'] = df_post_date.apply(lambda row: bought_each_day(row), axis=1)

df_post_date['Cumulative Buy'] = df_post_date['Daily Buy'].cumsum(axis=0)

#%%

df_post_date['Cumulative Dollars'] = df_post_date.apply(lambda row: dollars_each_day(row), axis=1)

# %%
x = df_post_date['Date']
y = df_post_date['Cumulative Dollars']
z = df_post_date['Cumulative Deposit']

plt.xlabel('Dates')
plt.ylabel('Dollars')
plt.title('Buying 5 dollars of BTC daily vs. sticking it under the mattress.')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=183))
plt.plot(x,y, '-b', label='BTC')
plt.plot(x,z, '-r', label='Mattress')
plt.legend()

for var in (y, z):
    plt.annotate('%0.2f' % var.max(), xy=(1, var.max()), xytext=(8, 0), 
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

plt.gcf().autofmt_xdate()