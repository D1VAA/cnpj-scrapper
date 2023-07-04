from __future__ import annotations

import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from typing import Union

from bcolors import Colors


class CNPJScrapper:
    def __init__(self, df, site):
        """
        :type site: str
        :type df: pd.DataFrame
        """
        self.exec = None
        self.verbose = None
        self.show_results = None
        self.outformat = None
        self.dataframe = df
        self.site = site
        self.name = dict()
        self.url = {'cnpj.biz': 'https://cnpj.biz/', 'speedio': 'https://api-publica.speedio.com.br/buscarcnpj?cnpj='}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

    async def _request(self, session, cnpj) -> [str, str, list]:
        url = self.url[self.site] + str(cnpj)
        try:
            async with session.get(url, headers=self.headers) as response:
                try:
                    response.raise_for_status()
                    r = await response.read()
                    return self.__parse_resp(cnpj, r)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    async def __parse_resp(self, cnpj, data) -> list or [str, str, list]:
        if 'speedio' in self.site:
            import json
            j = json.loads(data)
            infos = ['CNPJ', 'STATUS', 'SETOR', 'NOME FANTASIA', 'RAZAO SOCIAL', 'CNAE', 'CNAE PRINCIPAL CODIGO',
                     'EMAIL', 'DDD', 'TELEFONE', 'CEP']
            ext = [j[x] for x in infos]
            if self.verbose:
                print(f'{Colors.BG_RED}BUSCANDO{Colors.RESET}', end='\n\n')
                print(f'{Colors.RED}[+]{Colors.RESET} CNPJ : {Colors.RED}{cnpj}{Colors.RESET} >>>', end=' ')
                print(f'{Colors.BLUE}[-]{Colors.RESET} NOME : {Colors.BLUE}{ext[3]}{Colors.RESET}')
                print(f'{Colors.PURPLE}[*]{Colors.RESET} CNAES : {Colors.PURPLE}{ext[6]}{Colors.RESET}',
                      end='\n\n\n\n')
            return ext

        else:
            soup = BeautifulSoup(data, 'html.parser')
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

    async def __manage_requests(self) -> Union[dict[str, list], pd.Dataframe]:
        batches_size = 80
        results = list()
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    print('\n\n')
                    print(f'{Colors.PURPLE}[+]{Colors.RESET} Creating tasks...', end='\n\n')
                    b_tasks = [asyncio.create_task(self._request(session, company)) for _ in range(batches_size) for
                               company
                               in self.dataframe]
                    print(
                        f'{Colors.RED}[-]{Colors.RESET} Finished. >>> {Colors.CIAN}[-]{Colors.RESET} {len(b_tasks)} BATCHES',
                        end='\n\n')
                    print(f'{Colors.PURPLE}[+]{Colors.RESET} Sending packages...', end='\n\n')
                    for tasks in b_tasks:
                        result = await asyncio.gather(*tasks)
                        results.append(result)
                        await asyncio.sleep(2)

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

    def extract_export(self, results):
        companies = dict()
        for x in results:

            if self.show_results:
                print(f'{Colors.RED}[+]{Colors.RESET} COMPANY NAME : {Colors.RED}{name}{Colors.RESET} >>>',
                      end=' ')
                print(f'{Colors.YELLOW}[+]{Colors.RESET} CNPJ : {Colors.YELLOW}{cnpj}{Colors.RESET} >>>',
                      end=' ')
                print(f'{Colors.CIAN}[+]{Colors.RESET} CNAES : {Colors.CIAN}{cnaes}{Colors.RESET} >>>')

        self.dict_data = companies
        values = [(cnpj, cnaes) for cnpj, cnaes in companies.items()]
        dataframe = pd.DataFrame(values, columns=['cnpjs', 'cnaes'])
        return dataframe

    async def execute(self, show_results=False, verbose=False, outformat='dataframe'):
        self.show_results = show_results
        self.verbose = verbose
        self.outformat = outformat

        if outformat not in ['dataframe', 'dict']:
            raise ValueError("Invalid value for outformat. Allowed values are 'dataframe' and 'dict'.")

        execution = await self.__manage_requests()
        self.exec = execution
        return execution
