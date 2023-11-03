import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from packages.bcolors import Colors
from packages.email_extractor import email_extractor


async def parse_resp(i: list) -> pd.DataFrame:
    infos: list[str] = list()
    ext: list[dict] = list()
    try:
        # Extract infos depending on site option
        for index, data in enumerate(i):
            if 'cnpj.biz' in data['site']:
                #Section to extract data from the html
                #==================================

                soup = BeautifulSoup(data['response_html'], 'html.parser')
                title = [x.get_text() for x in soup.find_all('p') if 'Razão Social' in x.get_text()][0]
                c_name = title.replace('Razão Social: ', '')
                a_email = soup.find_all('a')
                emails = email_extractor(a_email)
                cnaes = soup.find_all('u')  # Company name
                cnaes = [''.join([x for x in cnae.get_text() if x.isdigit()]) for cnae in cnaes]
                infos = ['CNPJ', 'NOME', 'CNAES', 'EMAILS']  # Columns names
                values = [data['cnpj'], c_name, ', '.join(cnaes), emails]
                val = {x:y for x,y in zip(infos, values)}
                ext.append(val)
                if data['sw_res']:
                    print(f'Query Nº {index}')
                    print(f'{Colors.BLUE}[+]{Colors.RESET} NOME : {Colors.BLUE}{c_name}{Colors.RESET}')
                    print(f'{Colors.RED}[+]{Colors.RESET} CNPJ : {Colors.RED}{data["cnpj"]}{Colors.RESET}', end='\n')
                    print(f'{Colors.PURPLE}[+]{Colors.RESET} CNAES :', end=' ')
                    for cnae in cnaes:
                        print(f'{Colors.PURPLE}{cnae}{Colors.RESET}', end=' ')
                    print(f'\n{Colors.PURPLE}[@]{Colors.RESET} EMAILS : {emails}', end=' ')
                    print('\n\n')
                    await asyncio.sleep(1)
    except Exception as e:
        print('Exception occurred: ', e)
    
    df = pd.DataFrame(ext, columns=[x for x in infos])
    return df
