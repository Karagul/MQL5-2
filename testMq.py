from datetime import datetime
from MetaTrader5 import *
from pytz import timezone
import matplotlib.pyplot as plt
import pandas as pd #importa a Biblioteca do Pandas
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

menor = pd.read_csv('343265.positions.csv',delimiter=';') #Importa o arquivo 'menor.csv' e o salva como Data Frame em 'menor'
#df.to_csv('new-csv-file.csv') #Salva DataFrame em um arquivo csv...
print(type(menor)) #Imprime o tipo de var que estmos lidando
menor.info() #The method df.info() gives some statistics for each column.
menor.head() #Imprime as primeiras 5 linhas pra testar...só por quantas quer entre os parênteses
print(menor.Time[0])
datetime_object = datetime.strptime(menor.Time[0], '%Y.%m.%d %H:%M:%S')



utc_tz=timezone('UTC')

# connect to MetaTrader 5
MT5Initialize( )
# wait till MetaTrader 5 establishes connection to the trade server and synchronizes the environment
MT5WaitForTerminal( )

# request connection status and parameters
print(MT5TerminalInfo( ))
# get data on MetaTrader 5 version
print(MT5Version( ))

# request 1000 ticks from EURAUD
euraud_ticks=MT5CopyTicksFrom("EURAUD",datetime.utcnow(),1000,MT5_COPY_TICKS_ALL)
# request ticks from AUDUSD within 2019.04.01 13:00 - 2019.04.02 13:00
audusd_ticks=MT5CopyTicksRange("AUDUSD",datetime(2019,4,1,13),datetime(2019,4,2,13),MT5_COPY_TICKS_ALL)

# get bars from different symbols in a number of ways
eurusd_rates=MT5CopyRatesFrom(menor.loc[0,'Symbol'],MT5_TIMEFRAME_M1,datetime_object,1)

eurrub_rates=MT5CopyRatesFromPos("EURRUB",MT5_TIMEFRAME_M1,0,1000)
eurjpy_rates=MT5CopyRatesRange("EURJPY",MT5_TIMEFRAME_M1,datetime(2019,4,1,13),datetime(2019,4,2,13))
# shut down connection to MetaTrader 5
MT5Shutdown( )

# DATA
print('euraud_ticks(',len(euraud_ticks),')')
for val in euraud_ticks[:10]:
    print(val)

print('audusd_ticks(',len(audusd_ticks),')')
for val in audusd_ticks[:10]:
    print(val)
print('eurusdGetEnterRatesFromMQL(',len(eurusd_rates),')')
# for val in eurusdGetEnterRatesFromMQL[:10]:
#     print(val)
print(eurusd_rates)
print('eurrub_rates(',len(eurrub_rates),')')
for val in eurrub_rates[:10]:
    print(val)
print('eurjpy_rates(',len(eurjpy_rates),')')
for val in eurjpy_rates[:10]:
    print(val)

# PLOTTING
x_time=[x.time.astimezone(utc_tz) for x in euraud_ticks]
# prepare Bid and Ask arrays
bid=[y.bid for y in euraud_ticks]
ask=[y.ask for y in euraud_ticks]

# draw ticks on the chart
plt.plot(x_time,ask,'r-',label = 'ask')
plt.plot(x_time,bid,'g-',label = 'bid')
# display legends
plt.legend(loc = 'upper left')
# display header
plt.title('EURAUD ticks')
# display the chart
plt.show( )
#print(help(datetime))
print(datetime.utcnow())
print(datetime_object)


