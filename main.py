from __future__ import annotations
import pandas as pd
from packages.dfmanager.DataFrameManager import DataframeManager
from packages.scrapper import Scrapper
import asyncio
from argparse import ArgumentParser


parser = ArgumentParser(description='Executa uma busca em uma lista de CNPJs e retorna as informações das organizações')
parser.add_argument('-s', '--site', help='Seleciona o site que será feito a busca. Opções: cnpj.biz ou speedio')
args = parser.parse_args()
site = args.site

assert site is not None, 'Run: python ./main.py -h'

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


#cnaes = get_cnaes()
cnpjs = get_cnpjs()

consulta = Scrapper(cnpjs, site)
resultado = consulta.run(show_results=True)
resultado['CNAES'] = resultado['CNAES'].str.split(',')
resultado = resultado.explode('CNAES')
resultado.to_excel('Result.xlsx')

#filters = {'CNAES': cnaes}
#exp.apply_filters(filters)
