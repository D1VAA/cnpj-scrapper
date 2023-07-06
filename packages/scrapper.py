from __future__ import annotations

import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from typing import Union
from packages.html_manager import parse_resp

from packages.bcolors import Colors


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
                    print(
                        f'{Colors.YELLOW}|CONSULTA| [CNPJ] > {Colors.PURPLE}{cnpj}{Colors.RESET}',
                        end='\n\n')
                r = await response.read()
                result = await parse_resp(cnpj, r, self.site, self.verbose)
                self.dict_data.append(result)
            except Exception as e:
                print(e)

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
