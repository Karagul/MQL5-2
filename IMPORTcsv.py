import os
import pandas as pd
all_files=os.listdir('./')
for matFolder in all_files:
    if matFolder.endswith('.csv'):
        print(str(matFolder), "   <<< ---------------------------------------------------------------")
        print(type(matFolder))
        print((type('dadada.casa')))
        menor = pd.read_csv(matFolder, delimiter = ';')  # Importa o arquivo 'menor.csv' e o salva como Data Frame em 'menor'
