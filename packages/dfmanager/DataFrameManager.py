from typing import Iterator, Union, Dict, List
from os.path import getsize
import pandas as pd
from pandas import DataFrame, TextFileReader
from ..bcolors import Colors


class DataframeManager:
    """Classe para manipular dados de planilhas, incluindo aplicaçaão simples de filtros e tratamento de arquivos grandes."""

    # "https://www.listasdeempresa.com/criar"

    def __init__(self, path_file: str = None,
                 data: pd.DataFrame = None,
                 filters: dict[str, Union[list[str], str]] = None):
        self.path = path_file
        self.data = data
        self.filters = filters

        self.loaded_chunks = []  # List with all the chunks, for big sized files
        self.df = None  # Set a empty dataframe

    def __load_dataframe(self, chunksize: int or None) -> DataFrame | TextFileReader:
        if self.path.endswith('.csv'):
            return pd.read_csv(self.path, chunksize=chunksize)
            
        elif self.path.endswith('.xlsx'):
            return pd.read_excel(self.path)

    def get_dataframe(self, s: int=1, step: int=1) -> Union[DataFrame, Iterator]:
        """
        Método que retorna o dataframe. Para arquivos largos, retorna em chunks
        :param s: value * 1000 (lines to be read per time)
        """
        size_limit = 10 * 2 ** 20  # Tamanho limite do arquivo = 10 MB
        file_size = getsize(self.path)  # Pega o tamanho do arquivo

        if file_size > size_limit and self.path.endswith('.csv'):
            chunksize = s * 1000  # Define o tamanho das chunks 
            f_name = self.path[2:].capitalize()
            size = f'{file_size / 1024 / 1024:.2f}'
            print(
                f"{Colors.RED}[FILE]{Colors.RESET} {f_name:<13} {Colors.YELLOW}>>> {Colors.BLUE}[SIZE]{Colors.RESET} {size:<7} {Colors.YELLOW}>>>",
                end=' ')
            print(
                f"{Colors.PURPLE}[CHUNKS]{Colors.RESET} {chunksize * s} {Colors.UND_RED}LINES PER TIME{Colors.RESET}")
            iterator = self.__load_dataframe(chunksize)
            self.df = [next(iterator) for _ in range(step)][-1] 

        elif self.path.endswith('.xlsx'):
            f_name = self.path[2:].capitalize()
            size = f'{file_size / 1024 / 1024:.2f}'
            print(
                f"{Colors.RED}[FILE]{Colors.RESET} {f_name:<13} {Colors.YELLOW}>>> {Colors.BLUE}[SIZE]{Colors.RESET} \
                {size:<7} {Colors.YELLOW}>>>", end=' ')
            print(
                f"{Colors.PURPLE}[CHUNKS]{Colors.RESET} NO NEED")
            self.df = self.__load_dataframe()
        self.apply_filters(self.filters)

        return self.df

    def apply_filters(self, filters: Dict[str, Union[List[str], str]] = None) -> None:
        """
        Aplica os filtros especificados ao dataframe atual.
        Args:
            filters (dict[str, Union[list[str], str]]): Um dicionário onde a chave é o nome da coluna e os valores são os filtros a serem aplicados à coluna.
            Os filtros podem ser uma lista de strings ou uma string única.
        """
        assert filter is not None, ("Invalid filter.")
            
        first_key = list(filters.keys())[0]
        if not isinstance(filters[first_key], list) and filters is not None:
            try:
                for k, v in filters.items():
                    filters.update({k: v.tolist()})
            except:
                for k, v in filters.items():
                    filters.update({k: list(v)})

        repl = ';/.,-\\=-!@#$%¨&*()`[]?:|'
        empty_str = ' ' * len(repl)
        table = str.maketrans(repl, empty_str)

        filters = {k.translate(table): [val.translate(table) for val in v] for k, v in filters.items()}
        for col, cond in filters.items():
            try:
                if isinstance(cond, list):
                    self.df = self.df[self.df[col].isin(cond)]
                else:
                    self.df = self.df[col] == cond

            except KeyError as e:
                print('Ocorreu um erro tentando aplicar os filtros')
                print('Nome de coluna não encontrado: ', e)
