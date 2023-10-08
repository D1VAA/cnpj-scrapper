import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from packages.bcolors import Colors


async def parse_resp(cnpj, data, site, verbose) -> list or [str, str, list]:
    if 'speedio' in site:
        print('Executou')
        import json
        j = json.loads(data)
        infos = ['CNPJ', 'STATUS', 'SETOR', 'NOME FANTASIA', 'RAZAO SOCIAL', 'CNAE', 'CNAE PRINCIPAL CODIGO',
                 'EMAIL', 'DDD', 'TELEFONE', 'CEP']
        ext = {x: j[x] for x in infos}
        if verbose:
            print(f'{Colors.BLUE}[-]{Colors.RESET} NOME : {Colors.BLUE}{ext["NOME FANTASIA"]}{Colors.RESET}')
            print(f'{Colors.PURPLE}[*]{Colors.RESET} CNAES : ', end='')
            print(f'{Colors.PURPLE}{ext["CNAE PRINCIPAL CODIGO"]},{Colors.RESET}', end='\n\n\n\n')
        df = pd.DataFrame(ext, columns=[x for x in infos])
        return df

    elif 'cnpj.biz' in site:
        soup = BeautifulSoup(data, 'html.parser')
        title = [x.get_text() for x in soup.find_all('p') if 'Razão Social' in x.get_text()][0]
        c_name = title.replace('Razão Social: ', '')
        cnaes = soup.find_all('u')
        cnaes = [''.join([x for x in cnae.get_text() if x.isdigit()]) for cnae in cnaes]
        if verbose:
            print(f'{Colors.BLUE}[-]{Colors.RESET} NOME : {Colors.BLUE}{c_name}{Colors.RESET}')
            print(f'{Colors.RED}[+]{Colors.RESET} CNPJ : {Colors.RED}{cnpj}{Colors.RESET}', end='\n')
            print(f'{Colors.PURPLE}[*]{Colors.RESET} CNAES :', end=' ')
            for cnae in cnaes:
                print(f'{Colors.PURPLE}{cnae},{Colors.RESET}', end=' ')
            print('\n\n\n\n')
        ext = {'NOME': c_name, 'CNPJ': cnpj, 'CNAES': cnaes}
        df = pd.DataFrame(ext, columns=['NOME', 'CNPJ', 'CNAES'])
        return df
