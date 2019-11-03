from datetime import datetime
from MetaTrader5 import *
from pytz import timezone
import numpy as np
import os
import pandas as pd #importa a Biblioteca do Pandas
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#Compara todos os arquivos .csv na pasta

#Programa que checa todas as operações de entrada e saida
#Ele compara o preço de entrada e saida com o candlestick(range) de minuto (que possui high e low)
#Se estiver dentro das fronteiras eh pq eh real....
#Aperfeiçoar depois....

utc_tz=timezone('UTC')

# connect to MetaTrader 5
MT5Initialize( )
# wait till MetaTrader 5 establishes connection to the trade server and synchronizes the environment
MT5WaitForTerminal( )
# request connection status and parameters
#print(MT5TerminalInfo( ))
# get data on MetaTrader 5 version
#print(MT5Version( ))


baseStr='./csv/'
all_files=os.listdir(baseStr)
highestSumOfProfitVol=0
highestSignalSumOfProfitVol=""

for FileName in all_files: #Itera cada arquivo da pasta
    if FileName.endswith('.csv'): #Checa se eh um arquivo CSV
        print(str(FileName),"   <<< ---------------------------------------------------------------")
        menor = pd.read_csv(baseStr+FileName,delimiter = ';')  # Importa o arquivo 'menor.csv' e o salva como Data Frame em 'menor'

        timeframe=MT5_TIMEFRAME_M5
        contaBuySell=0
        contaEntradasDentroDaFronteira=0
        contaSaidasDentroDaFronteira=0

        sumProfitVolume=0

        highestVariation=0
        for linha in range(len(menor)):
            if not np.isnan(menor.loc[linha,'Volume']):
                #Calculate the sum of all profit/volume
                profit=menor.loc[linha,'Profit']
                volume=menor.loc[linha,'Volume']
                sumProfitVolume+= profit/volume
                #print(str(profit/volume))


            # Aqui acessa o range do timedate e compara ele com o preco de entrada e saida e a porcentagem de desvio ....
            try:
                if not np.isnan(menor.loc[linha,'Volume']):
                    contaBuySell+=1
                    # print(menor.loc[linha,'Symbol'])
                    #Convert the time string onto a object of datetime
                    datetime_object = datetime.strptime(menor.Time[linha], '%Y.%m.%d %H:%M:%S')
                    # print(datetime_object)
                    #print(menor.info())
                    #print(menor.loc[linha,'Time.1'])
                    datetime_object1 = datetime.strptime(menor.loc[linha,'Time.1'], '%Y.%m.%d %H:%M:%S')
                    # print(datetime_object1)
                    # get bars from different symbols in a number of ways
                    eurusdGetEnterRatesFromMQL=MT5CopyRatesFrom(menor.loc[linha,'Symbol'],timeframe,datetime_object,1)
                    eurusdGetOutRatesFromMQL=MT5CopyRatesFrom(menor.loc[linha,'Symbol'],timeframe,datetime_object1,1)


                    ratesEntrada = pd.DataFrame(list(eurusdGetEnterRatesFromMQL),
                                                columns=['time', 'open', 'low', 'high', 'close', 'tick_volume', 'spread', 'real_volume'])
                    ratesSaida = pd.DataFrame(list(eurusdGetOutRatesFromMQL),
                                                columns=['time', 'open', 'low', 'high', 'close', 'tick_volume', 'spread', 'real_volume'])

                    # print(eurusdGetEnterRatesFromMQL)
                    # print(eurusdGetOutRatesFromMQL)
                    # print(menor.loc[linha,:])
                    # print(ratesEntrada.loc[0,'low'])
                    # print(menor.loc[linha,'Price'])
                    # print(ratesEntrada.loc[0,'high'])
                    # print("---------------------------")
                    # print(ratesSaida.loc[0,'low'])
                    # print(menor.loc[linha,'Price.1'])
                    # print(ratesSaida.loc[0,'high'])

                    # print(datetime.utcnow())
                    # print(datetime_object)
                    # for lin in eurusdGetEnterRatesFromMQL:
                    #     print(lin)
                    #     print(type(lin))
                    #     print(help(lin))
                    #     print(list(lin))
                    percentageOfVariationEntrada = ((ratesEntrada.loc[0,'low'])/(menor.loc[linha,'Price']))/100
                    percentageOfVariationSaida=((ratesEntrada.loc[0,'high']) / (menor.loc[linha,'Price'])) / 100
                    if highestVariation<percentageOfVariationEntrada:
                        highestVariation=percentageOfVariationEntrada
                    if highestVariation<percentageOfVariationSaida:
                        highestVariation=percentageOfVariationSaida

                    # print(linha, "  " , menor.loc[linha,'Symbol'], " Entrada ", str(ratesEntrada.loc[0,'low']),"   ", str(menor.loc[linha,'Price']),
                    #       "   ", str(ratesEntrada.loc[0,'high']),"  Percentage variation from low: ", str(percentageOfVariationSaida))
                    if menor.loc[linha,'Price'] <= ratesEntrada.loc[0,'low'] and menor.loc[linha,'Price'] >= ratesEntrada.loc[0,'high']:
                        # print("Entrada dentro das fronteiras na linha :  ", str(linha))
                        contaEntradasDentroDaFronteira+=1
                    if menor.loc[linha,'Price.1'] <= ratesSaida.loc[0,'low'] and menor.loc[linha,'Price.1'] >= ratesSaida.loc[0,'high']:
                        # print("Saida encontra-se dentro das fornteiras na linha :  ", str(linha))
                        contaSaidasDentroDaFronteira+=1

                    if highestSumOfProfitVol<sumProfitVolume:
                        highestSumOfProfitVol=sumProfitVolume
                        highestSignalSumOfProfitVol=FileName
                pass
            except:
                # print("Pulei uma linha em: ", FileName, " com o simbolo: ", menor.loc[linha,'Symbol'])
                continue
                    # if ratesEntrada.loc[0,'low']>=menor.loc[linha,'Price']>=ratesEntrada.loc[0,'high'] and ratesSaida.loc[0,'low']>=menor.loc[linha,'Price.1']>=ratesSaida.loc[0,'high'] :
                    #     print("Entrada e Saida dentro das fronteiras na linha :  ", str(linha))
            #Aqui ele guarda o com maior proporcao profit/volume .... mas como tem alguns sinais que operam em ooutras coisas alem de moedas...
            #Fudeu .....


        print("De um total de : ", str(contaBuySell), " Entradas e Saidas")
        print(" somente ", str(contaEntradasDentroDaFronteira), " Entradas e     ", str(contaSaidasDentroDaFronteira), " Saidas dentro das fronteiras")
        print("Highest Variation is :", str(highestVariation))
        print(" O somatorio do Profit/Volume eh: ", str(sumProfitVolume))

#Deu Ruim ja que alguns ativos negociados tem valor do volume diferente....solucao seria calcular Profit/ValueOfTheVolume
#Como calcular o valor em USD do volume ???? :/
print("-------------------- The Signal with higest somatorio of Profit/Volume is :", highestSignalSumOfProfitVol, "   wich is : ", str(highestSumOfProfitVol))

MT5Shutdown( )

