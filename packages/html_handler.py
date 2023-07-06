import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from packages.bcolors import Colors


async def parse_resp(i: list) -> pd.DataFrame:
    infos: list[str] = list()
    ext: list[dict] = list()
    try:
        for data in i:
            if 'speedio' in data['site']:
                import json
                j = json.loads(data['r'])
                infos = ['CNPJ', 'STATUS', 'SETOR', 'NOME FANTASIA',
                         'RAZAO SOCIAL', 'CNAE', 'CNAE PRINCIPAL CODIGO',
                         'EMAIL', 'DDD', 'TELEFONE', 'CEP']
                val = {x: j[x] for x in infos}
                ext.append(val)
                if data['sw_res']:
                    print(f'{Colors.BLUE}[-]{Colors.RESET} NOME : {Colors.BLUE}{ext["NOME FANTASIA"]}{Colors.RESET}')
                    print(f'{Colors.RED}[+]{Colors.RESET} CNPJ : {Colors.RED}{data["cnpj"]}{Colors.RESET}', end='\n')
                    print(f'{Colors.PURPLE}[*]{Colors.RESET} CNAES : ', end='')
                    print(f'{Colors.PURPLE}{ext["CNAE PRINCIPAL CODIGO"]},{Colors.RESET}', end='\n\n\n\n')

            elif 'cnpj.biz' in data['site']:
                soup = BeautifulSoup(data['r'], 'html.parser')
                title = [x.get_text() for x in soup.find_all('p') if 'Razão Social' in x.get_text()][0]
                c_name = title.replace('Razão Social: ', '')
                cnaes = soup.find_all('u')  # Company name
                cnaes = [''.join([x for x in cnae.get_text() if x.isdigit()]) for cnae in cnaes]
                infos = ['CNPJ', 'NOME', 'CNAES']  # Columns names
                values = [data['cnpj'], c_name, ', '.join(cnaes)]
                val = {x:y for x,y in zip(infos, values)}
                ext.append(val)
                if data['sw_res']:
                    print(f'{Colors.BLUE}[-]{Colors.RESET} NOME : {Colors.BLUE}{c_name}{Colors.RESET}')
                    print(f'{Colors.RED}[+]{Colors.RESET} CNPJ : {Colors.RED}{data["cnpj"]}{Colors.RESET}', end='\n')
                    print(f'{Colors.PURPLE}[*]{Colors.RESET} CNAES :', end=' ')
                    for cnae in cnaes:
                        print(f'{Colors.PURPLE}|{cnae}|{Colors.RESET}', end=' ')
                    print('\n\n\n\n')
    except Exception:
        pass
    
    df = pd.DataFrame(ext, columns=[x for x in infos])
    return df
