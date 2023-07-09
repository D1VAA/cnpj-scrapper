from __future__ import annotations
import pandas as pd
import asyncio
from packages.dfmanager.DataFrameManager import DataframeManager
from packages.scrapper import Scrapper
from menu import MenuConstructor


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


def get_cnpjs(size=1):
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


menu = MenuConstructor()
menu.add_option('cnpjs', func=get_cnpjs)
menu.add_option('cnaes', func=get_cnaes)
menu._menu()
# menu.add_option(['exec'], attr=consulta.run(show_results=True))

# resultado = consulta.run(show_results=True)
# resultado['CNAES'] = resultado['CNAES'].str.split(',')
# resultado = resultado.explode('CNAES')
# resultado.to_excel('Result.xlsx')
