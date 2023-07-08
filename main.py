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
    :param size: value * 1000 (lines)
    """
    filterlist = {'uf': ['SP', 'SC', 'RS']}
    data = DataframeManager('./sheets/empresas.csv', filters=filterlist)
    g_dataframe = data.get_dataframe(size)

    # Select cnpj column
    dataframe = g_dataframe['cnpj']
    return dataframe


def exec(parametro=None):
    """
    Função para teste
    """
    print("Teste!")


menu = MenuConstructor()
menu.add_option('exec', attr=exec)
menu.run()
# menu.add_option(['exec'], attr=consulta.run(show_results=True))

# resultado = consulta.run(show_results=True)
# resultado['CNAES'] = resultado['CNAES'].str.split(',')
# resultado = resultado.explode('CNAES')
# resultado.to_excel('Result.xlsx')
