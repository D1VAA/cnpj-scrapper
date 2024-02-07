import pandas as pd
from pandas import DataFrame
from packages.dfmanager.DataFrameManager import DataframeManager
from packages.scrapper import Scrapper
from packages.download_files import download_cnaes, download_empresas
from os.path import exists

def get_cnaes() -> DataFrame:
    file_path = './CNAES.xlsx'
    if exists(file_path):
        filterlist = {'Atividade': ['Comércio', 'Indústria']}
        data = DataframeManager(file_path, filters=filterlist)
        dataframe = data.get_dataframe()

        # Splitting information
        cnae_split = dataframe['CNAE'].str.split(' – ', n=1, expand=True)
        dataframe['Código'] = cnae_split[0]
        dataframe['Descrição'] = cnae_split[1]

        # Removing useless columns
        dataframe = dataframe.drop(columns=['Anexo', 'Tributação', 'FatorR', 'Alíq.(%)'], axis=1)
        return dataframe
    else:
        download_cnaes()
        get_cnaes()


def get_cnpjs(size: int = 1) -> DataFrame:
    """
    Function that read the cnpjs of the file 'empresas.csv'
    =======
    Args:

    :parameter size: Receive a integer number and multiply by 1.000 (represents the lines to be read)
    """
    file_path = './empresas.csv'
    if exists(file_path):
        filterlist = {'uf': ['SP', 'SC', 'RS']}
        data = DataframeManager(file_path, filters=filterlist)
        g_dataframe = data.get_dataframe(size, step=1)
        dataframe = g_dataframe['cnpj']
        return dataframe
    else:
        download_empresas()
        get_cnpjs()

    # Select cnpj column

# scrap = Scrapper(cnpjs, 'cnpj.biz', show_results=True, verbose=False) # Setup the scrapper
# results = scrap.run()

# results['CNAES'] = results['CNAES'].str.split(',')
# results = results.explode('CNAES')
# results.to_excel('Result.xlsx')
