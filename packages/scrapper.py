from __future__ import annotations

import aiohttp
import asyncio
import pandas as pd
from packages.html_handler import parse_resp

from packages.bcolors import Colors


class Scrapper:
    def __init__(self, df, site):
        """
        :type site: str
        :type df: pd.DataFrame
        """
        self.verbose: bool = None
        self.show_results: bool = None
        self.outformat = None  # For later implementation
        self.dataframe: pd.DataFrame = df
        self.site: str = site
        self.result: pd.DataFrame = None
        self.dict_data: list[dict] = list()
        self.url = {'cnpj.biz': 'https://cnpj.biz/', 'speedio': 'https://api-publica.speedio.com.br/buscarcnpj?cnpj='}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }

    async def _request(self, session, cnpj) -> [str, str, list]:
        url = self.url[self.site] + str(cnpj)
        async with session.get(url, headers=self.headers) as response:
            try:
                response.raise_for_status()
                if self.verbose:
                    print(
                        f'{Colors.YELLOW}|CONSULTA| [CNPJ] > {Colors.PURPLE}{cnpj}{Colors.RESET}',
                        end='\n\n')
                r = await response.read() # Site Response (HTML)
                #print(response.status)
                # Save cnpj, site response, site name show_results option (verbose)
                self.dict_data.append({'cnpj': cnpj, 'response_html': r, 'site': self.site, 'sw_res': self.show_results})

            except Exception as e:
                print(e)

    async def __manage_requests(self):
        try:
            async with aiohttp.ClientSession() as session:
                print('\n\n')
                print(f'{Colors.PURPLE}[+]{Colors.RESET} Creating tasks...', end='\n\n')
                batch_size = 3
                total_batches = len(self.dataframe) // batch_size + 1
                print(f'{Colors.PURPLE}[+]{Colors.RESET} Starting queries...', end='\n\n')
                for i in range(total_batches):
                    print(
                        f'\n{Colors.RED}[-]{Colors.RESET} Batch Nº >>> {Colors.CIAN}{i+1}{Colors.RESET}',
                        end='\n\n')
                    start_i = i * batch_size
                    end_i = min(start_i + batch_size, len(self.dataframe))
                    batch_data = self.dataframe[start_i:end_i]
                    tasks = [asyncio.create_task(self._request(session, cnpj)) for cnpj in batch_data]
                    await asyncio.gather(*tasks)
                    await asyncio.sleep(4)
        except Exception as e:
            print(f"An exception occurred... {str(e)[:50]}")

        # Parse results after all the execution
        self.result = await parse_resp(self.dict_data)

    def run(self, show_results=False, verbose=False, outformat='dataframe'):
        self.show_results = show_results
        self.verbose = verbose
        self.outformat = outformat

        if outformat not in ['dataframe', 'dict']:
            raise ValueError("Invalid value for outformat. Allowed values are 'dataframe' and 'dict'.")
        asyncio.run(self.__manage_requests())
        return self.result
