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
        self.dict_data = list()
        self.url = {'cnpj.biz': 'https://cnpj.biz/', 'speedio': 'https://api-publica.speedio.com.br/buscarcnpj?cnpj='}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

    async def _request(self, session, cnpj) -> [str, str, list]:
        url = self.url[self.site] + str(cnpj)
        async with session.get(url, headers=self.headers) as response:
            try:
                response.raise_for_status()
                if self.verbose:
                    print(f'{Colors.BG_RED}BUSCANDO{Colors.RESET}', end='\n\n')
                    print(f'{Colors.RED}[+]{Colors.RESET} CNPJ : {Colors.RED}{cnpj}{Colors.RESET} >>>', end=' ')
                r = await response.read()
                return await self.__parse_resp(cnpj, r)
            except Exception as e:
                print(e)

    async def __parse_resp(self, cnpj, data) -> list or [str, str, list]:
        if 'speedio' in self.site:
            import json
            j = json.loads(data)
            infos = ['CNPJ', 'STATUS', 'SETOR', 'NOME FANTASIA', 'RAZAO SOCIAL', 'CNAE', 'CNAE PRINCIPAL CODIGO',
                     'EMAIL', 'DDD', 'TELEFONE', 'CEP']
            ext = {x: j[x] for x in infos}
            if self.verbose:
                print(f'{Colors.BLUE}[-]{Colors.RESET} NOME : {Colors.BLUE}{ext["NOME FANTASIA"]}{Colors.RESET}')
                print(
                    f'{Colors.PURPLE}[*]{Colors.RESET} CNAES : {Colors.PURPLE}{ext["CNAE PRINCIPAL CODIGO"]}{Colors.RESET}',
                    end='\n\n\n\n')
            self.dict_data.append(ext)
            return ext

        else:
            soup = BeautifulSoup(data, 'html.parser')
            title = [x.get_text() for x in soup.find_all('p') if 'Razão Social' in x.get_text()][0]
            c_name = title.replace('Razão Social: ', '')
            cnaes = soup.find_all('u')
            cnaes = [''.join([x for x in cnae.get_text() if x.isdigit()]) for cnae in cnaes]
            if self.verbose:
                print(f'{Colors.BLUE}[-]{Colors.RESET} NOME : {Colors.BLUE}{c_name}{Colors.RESET}')
                print(f'{Colors.PURPLE}[*]{Colors.RESET} CNAES :', end=' ')
                for cnae in cnaes:
                    print(f'{Colors.PURPLE}{cnae}{Colors.RESET}', end=' ')
                print('\n\n\n\n')
            ext = {'NOME': c_name, 'CNPJ': cnpj, 'CNAES': cnaes}
            self.dict_data.append(ext)
            return ext

    async def __manage_requests(self):
        try:
            async with aiohttp.ClientSession() as session:
                print('\n\n')
                print(f'{Colors.PURPLE}[+]{Colors.RESET} Creating tasks...', end='\n\n')
                batch_size = 30
                total_batches = len(self.dataframe) // batch_size + 1
                for i in range(total_batches):
                    start_i = i * batch_size
                    end_i = min(start_i + batch_size, len(self.dataframe))
                    batch_data = self.dataframe[start_i:end_i]

                    tasks = [asyncio.create_task(self._request(session, cnpj)) for cnpj in batch_data]
                    print(
                        f'{Colors.RED}[-]{Colors.RESET} Finished. >>> {Colors.CIAN}[-]{Colors.RESET}',
                        end='\n\n')
                    print(f'{Colors.PURPLE}[+]{Colors.RESET} Sending packages...', end='\n\n')
                    await asyncio.gather(*tasks)
                    await asyncio.sleep(2)

        except Exception:
            pass

    async def execute(self, show_results=False, verbose=False, outformat='dataframe'):
        self.show_results = show_results
        self.verbose = verbose
        self.outformat = outformat

        if outformat not in ['dataframe', 'dict']:
            raise ValueError("Invalid value for outformat. Allowed values are 'dataframe' and 'dict'.")

        await self.__manage_requests()

        return self.dict_data
