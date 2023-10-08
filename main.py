from __future__ import annotations
import pandas as pd
import asyncio
from packages.dfmanager.DataFrameManager import DataframeManager
from packages.scrapper import Scrapper
from packages.menu_constructor.menu import MenuConstructor


def get_cnaes():
    filterlist = {'Atividade': ['Comércio', 'Indústria']}
    data = DataframeManager('./sheets/CNAES.xlsx', filters=filterlist)
    dataframe = data.get_dataframe()

    # Splitting information
    cnae_split = dataframe['CNAE'].str.split(' – ', n=1, expand=True)
    dataframe['Código'] = cnae_split[0]
    dataframe['Descrição'] = cnae_split[1]

    # Removing useless columns
    dataframe = dataframe.drop(columns=['Anexo', 'Tributação', 'FatorR', 'Alíq.(%)'], axis=1)
    return dataframe


def get_cnpjs(size: int = 1):
    """
    Function that read the cnpjs of the file 'empresas.csv'
    =======
    Args:

    :parameter size: Receive a integer number and multiply by 1.000 (represents the lines to be read)
    """
    filterlist = {'uf': ['SP', 'SC', 'RS']}
    data = DataframeManager('./sheets/empresas.csv', filters=filterlist)
    g_dataframe = data.get_dataframe(size)

    # Select cnpj column
    dataframe = g_dataframe['cnpj']
    return dataframe

scrap = Scrapper(get_cnpjs(), 'cnpj.biz')
results = scrap.run(verbose=True, show_results=True)
print(results)

results['CNAES'] = results['CNAES'].str.split(',')
results = results.explode('CNAES')
results.to_excel('Result.xlsx')
