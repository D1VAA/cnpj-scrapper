import pandas as pd
from pandas import DataFrame
from packages.dfmanager.DataFrameManager import DataframeManager
from packages.scrapper import Scrapper

def get_cnaes() -> DataFrame:
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


def get_cnpjs(size: int = 1) -> DataFrame:
    """
    Function that read the cnpjs of the file 'empresas.csv'
    =======
    Args:

    :parameter size: Receive a integer number and multiply by 1.000 (represents the lines to be read)
    """
    filterlist = {'uf': ['SP', 'SC', 'RS']}
    data = DataframeManager('./sheets/empresas.csv', filters=filterlist)
    g_dataframe = data.get_dataframe(size, step=1)

    # Select cnpj column
    dataframe = g_dataframe['cnpj']
    return dataframe

# cnpjs = get_cnpjs()
# scrap = Scrapper(cnpjs, 'cnpj.biz', show_results=True, verbose=False) # Setup the scrapper
# results = scrap.run()

# results['CNAES'] = results['CNAES'].str.split(',')
# results = results.explode('CNAES')
# results.to_excel('Result.xlsx')
