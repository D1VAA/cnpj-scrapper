from __future__ import annotations
from dfManager import DataframeManager
import asyncio
import aiohttp


def get_cnaes():
    filterlist = {'Atividade': ['Comércio', 'Indústria']}
    data = DataframeManager('./CNAES.xlsx', filterlist)
    dataframe = data.get_dataframe()

    # Splitting information
    cnae_split = dataframe['CNAE'].str.split(' – ', n=1, expand=True)
    dataframe['Código'] = cnae_split[0]
    dataframe['Descrição'] = cnae_split[1]

    # Removing useless columns
    dataframe = dataframe.drop(columns=['Anexo', 'Tributação', 'FatorR', 'Alíq.(%)'], axis=1)
    return dataframe


def get_cnpjs():
    filterlist = {'uf': ['SP', 'SC', 'RS']}
    data = DataframeManager('./empresas.csv', filterlist)
    g_dataframe = data.get_dataframe()

    # Select cnpj column
    dataframe = g_dataframe['cnpj']
    return dataframe


cnaes = get_cnaes()
cnpjs = get_cnpjs()

class SearchCNPJ():
    