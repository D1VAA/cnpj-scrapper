import aiohttp
import asyncio
import pandas as pd
from packages.html_handler import Parser
from os.path import getsize, isfile
from time import sleep

from packages.bcolors import Colors


class Scrapper:
    def __init__(self, df: pd.DataFrame, site: str, show_results: bool=False, verbose: bool=False):
        self.verbose: bool = verbose
        self.show_results: bool = show_results
        self.outformat = None  # For later implementation
        self.dataframe: pd.DataFrame = df
        self.site: str = site
        self.result: pd.DataFrame = None
        self.dict_data: list[dict] = list()
        self.url = {'cnpj.biz': 'https://cnpj.biz/'}
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
                        f'{Colors.GREEN}[ OK ]{Colors.RESET} CNPJ: {cnpj}')
                r = await response.read() # Site Response (HTML)
                # Save cnpj, site response, site name show_results option (verbose)
                self.dict_data.append({'cnpj': cnpj, 
                                       'response_html': r, 
                                       'site': self.site, 
                                       'sw_res': self.show_results})
            except Exception:
                print(f'{Colors.RED}[ ERROR ]{Colors.RESET} CNPJ: {cnpj}')

    async def __manage_requests(self):
        try:
            async with aiohttp.ClientSession() as session:
                print('\n\n')
                print(f'{Colors.GREEN}[ OK ]{Colors.RESET} Creating tasks...', end='\n')
                sleep(1)
                batch_size = 3
                total_batches = len(self.dataframe) // batch_size + 1
                print('Total Batches: ', total_batches)
                print(f'{Colors.BLUE}[ + ]{Colors.RESET} Starting queries...', end='\n\n')
                for i in range(total_batches):
                    print(f'[-] Batch Nº: {i+1}')
                    start_i = i * batch_size
                    end_i = min(start_i + batch_size, len(self.dataframe))
                    batch_data = self.dataframe[start_i:end_i]
                    tasks = [asyncio.create_task(self._request(session, cnpj)) for cnpj in batch_data]
                    await asyncio.gather(*tasks)
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"An exception occurred... {str(e)[:50]}")

        print('Total...', len(self.dict_data))
        self.result = Parser(self.dict_data).parse_resp()

    def run(self):
        asyncio.run(self.__manage_requests())
        return self.result
