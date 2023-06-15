from __future__ import annotations
from typing import Iterator, Union
from os.path import getsize
import pandas as pd
from pandas import DataFrame


# url = 'https://api-publica.speedio.com.br/buscarcnpj?cnpj=00000000000191'
# "https://www.listasdeempresa.com/criar"


class DataframeManager:
    def __init__(self, path: str, filters: dict[str, Union[list[str], str]] = None):
        self.path = path  # Path to file
        self.filters = filters
        self.chunksize = None
        self.iterator = None

        self.loaded_chunks = []  # List with all the chunks
        self.df = None  # Set a empty dataframe

    def __load_dataframe(self, chunksize: int | None = None) -> DataFrame | iter:
        if self.path.endswith('.csv'):
            return pd.read_csv(self.path, chunksize=chunksize)

        elif self.path.endswith('.xlsx'):
            return pd.read_excel(self.path)

    def __iter__(self):
        pass
    
    def __next__(self):
        try:
            chunk = next(self.iterator)
            self.loaded_chunks.append(chunk)
            self.df = pd.concat(self.loaded_chunks)
            self.apply_filters(self.filters)
            
            return self.df
            
        except StopIteration:
            raise StopIteration

    def get_dataframe(self) -> Union[DataFrame, Iterator]:
        size_limit = 10 * 2 ** 20  # Tamanho limite do arquivo = 10 MB
        file_size = getsize(self.path)  # Pega o tamanho do arquivo

        if file_size > size_limit and self.path.endswith('.csv'):
            print("Arquivo: ", self.path, "Tamanho: ", file_size, "Limite: ", size_limit, end='\n')
            self.chunksize = 10 ** 6  # Define o tamanho das chunks (1 milhão de linhas)
            self.iterator = self.__load_dataframe(self.chunksize)
            self.__next__()

        elif self.path.endswith('.xlsx'):
            print("Arquivo: ", self.path, "Tamanho: ", file_size, "Limite: ", size_limit, end='\n')
            self.df = self.__load_dataframe()
            self.apply_filters(self.filters)

        return self.df

    def apply_filters(self, filters: dict[str, Union[list[str], str]] | None) -> DataFrame:
        """
        Aplica os filtros especificados ao dataframe atual.
        Args:
            filters (dict[str, Union[list[str], str]]): Um dicionário onde a chave é o
                nome da coluna e os valores são os filtros a serem aplicados à coluna.
                Os filtros podem ser uma lista de strings ou     uma string única.
        Returns:    
            DataframeManager: Retorna uma instância da classe DataframeManager com
                o dataframe atualizado.
        """

        if filters is not None:
            for col, cond in filters.items():
                try:
                    if isinstance(cond, list):
                        condition = self.df[col].isin(cond)
                    else:
                        condition = self.df[col] == cond
                    self.df = self.df[condition]

                except KeyError as e:
                    print('Ocorreu um erro tentando aplicar os filtros')
                    print('Nome de coluna não encontrado: ', e)

        return self.df
