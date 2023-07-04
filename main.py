from __future__ import annotations
<<<<<<< HEAD

from typing import Union

from dfManager import DataframeManager
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from bcolors import Colors
import pandas as pd
from time import sleep
=======
from dfManager import DataframeManager
import asyncio
import aiohttp
>>>>>>> 6292c2ac87a3506955a685b7ab8ef7f4c46b37c6


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


<<<<<<< HEAD
# cnaes = get_cnaes()
cnpjs = get_cnpjs()


class CNPJScrapper:
    def __init__(self, df, site='cnpj.biz'):
        self.dataframe = df
        self.site = site
        self.name = dict()
        self.url = {'cnpj.biz': 'https://cnpj.biz/'}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

    async def _request(self, session, cnpj) -> [str, str, list]:
        url = self.url[self.site] + str(cnpj)
        try:
            async with session.get(url, headers=self.headers) as response:
                try:
                    response.raise_for_status()
                    r = await response.read()
                    soup = BeautifulSoup(r, 'html.parser')
                    title = [x.get_text() for x in soup.find_all('p') if 'Razão Social' in x.get_text()][0]
                    c_name = title.replace('Razão Social: ', '')
                    cnaes = soup.find_all('u')
                    cnaes = [''.join([x for x in cnae.get_text() if x.isdigit()]) for cnae in cnaes]
                    if self.verbose:
                        print(f'{Colors.BG_RED}BUSCANDO{Colors.RESET}', end='\n\n')
                        print(f'{Colors.RED}[+]{Colors.RESET} CNPJ : {Colors.RED}{cnpj}{Colors.RESET} >>>', end=' ')
                        print(f'{Colors.BLUE}[-]{Colors.RESET} NOME : {Colors.BLUE}{c_name}{Colors.RESET}')
                        print(f'{Colors.PURPLE}[*]{Colors.RESET} CNAES : {Colors.PURPLE}{cnaes}{Colors.RESET}',
                              end='\n\n\n\n')
                    return c_name, cnpj, cnaes
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    async def __manage_requests(self) -> Union[dict[str, list], pd.Dataframe]:
        companies = dict()
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    print('\n\n')
                    print(f'{Colors.PURPLE}[+]{Colors.RESET} Creating tasks...', end='\n\n')
                    tasks = [asyncio.create_task(self._request(session, company)) for company in self.dataframe]
                    print(f'{Colors.RED}[-]{Colors.RESET} Finished.', end='\n\n')
                    print(f'{Colors.PURPLE}[+]{Colors.RESET} Initializing requests...', end='\n\n')
                    sleep(2)
                    results = await asyncio.gather(*tasks)
                    for name, cnpj, cnaes in results:
                        companies[cnpj] = cnaes
                        self.name[cnpj] = name
                        if self.show_results:
                            print(f'{Colors.RED}[+]{Colors.RESET} COMPANY NAME : {Colors.RED}{name}{Colors.RESET} >>>',
                                  end=' ')
                            print(f'{Colors.YELLOW}[+]{Colors.RESET} CNPJ : {Colors.YELLOW}{cnpj}{Colors.RESET} >>>',
                                  end=' ')
                            print(f'{Colors.CIAN}[+]{Colors.RESET} CNAES : {Colors.CIAN}{cnaes}{Colors.RESET} >>>')

                    if self.outformat == 'dict':
                        return companies
                    values = [(cnpj, cnaes) for cnpj, cnaes in companies.items()]
                    dataframe = pd.DataFrame(values, columns=['cnpjs', 'cnaes'])
                    return dataframe

                except Exception as e:
                    print(e)

                finally:
                    if self.outformat == 'dict':
                        return companies
                    values = [(cnpj, cnaes) for cnpj, cnaes in companies.items()]
                    dataframe = pd.DataFrame(values, columns=['cnpjs', 'cnaes'])
                    return dataframe
        except Exception:
            pass

    async def execute(self, show_results=False, verbose=False, outformat='dataframe'):
        self.show_results: bool = show_results
        self.verbose: bool = verbose
        self.outformat = outformat

        if outformat not in ['dataframe', 'dict']:
            raise ValueError("Invalid value for outformat. Allowed values are 'dataframe' and 'dict'.")

        execution = await self.__manage_requests()
        self.exec = execution
        return execution


a = CNPJScrapper(cnpjs)
resultado = asyncio.run(a.execute(verbose=True, show_results=True))
print(resultado)
resultado.to_excel('CNPJS_x_CNAES.xlsx')
=======
cnaes = get_cnaes()
cnpjs = get_cnpjs()

class SearchCNPJ():
    
>>>>>>> 6292c2ac87a3506955a685b7ab8ef7f4c46b37c6
