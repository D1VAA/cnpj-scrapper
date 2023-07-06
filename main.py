from __future__ import annotations
import pandas as pd
from packages.dfmanager.DataFrameManager import DataframeManager
from packages.scrapper import CNPJScrapper
import asyncio
from argparse import ArgumentParser


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
    return dataframe['Código']


def get_cnpjs(size=1):
    filterlist = {'uf': ['SP', 'SC', 'RS']}
    data = DataframeManager('./sheets/empresas.csv', filters=filterlist)
    g_dataframe = data.get_dataframe(size)

    # Select cnpj column
    dataframe = g_dataframe
    return dataframe['cnpj']


f_cnaes = get_cnaes()
cnpjs = get_cnpjs(1)

parser = ArgumentParser(description='Executa uma busca em uma lista de CNPJs e retorna as informações das organizações')
parser.add_argument('-s', '--site', help='Seleciona o site que será feito a busca. Opções: cnpj.biz ou speedio')
args = parser.parse_args()
site = args.site
assert site is not None, 'Run: python ./main.py -h'

consulta = CNPJScrapper(cnpjs, site)
resultado = asyncio.run(consulta.execute(verbose=True, show_results=True))
filters = {'CNAES': f_cnaes}
exp = DataframeManager(data=resultado)
exp.apply_filters(filters)
print(exp)
