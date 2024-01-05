from typing import List, Dict
import pandas as pd
from bs4 import BeautifulSoup
from packages.bcolors import Colors
from packages.email_extractor import email_extractor

class Parser:
    def __init__(self, data):
        self.data: Dict = data
        
    @staticmethod
    def _extract_title(soup) -> str:
        for x in soup.find_all('p'):
            x_text = x.get_text()
            if 'Razão Social' in x_text:
                return x_text.replace("Razão Social: ", '')

    @staticmethod
    def _extract_email(soup) -> List[str]:
        tag_a_email = soup.find_all('a')
        emails = email_extractor(tag_a_email)
        return emails
    
    @staticmethod
    def _extract_email(soup) -> List[str]:
        cnaes = soup.find_all('u')  # Company name
        cnaes = list()
        for cnae in cnaes:
            cnae_text = cnae.get_text()
            for x in cnae_text:
                if x.isdigit():
                    cnaes.append(''.join(x))
        return cnaes

    def parse_resp(self) -> pd.DataFrame:
        # Dictionary with all the data extracted saved in dictionarys.
        ext: List[Dict[str, str|List]] = list()
        try:
            for index, data in enumerate(self.data):
                site_name = data['site']
                if 'cnpj.biz' in site_name:
                    #Section to extract data from the html
                    #==================================

                    html = data['response_html']
                    soup = BeautifulSoup(html, 'html.parser')
                    company_name = self._extract_title(soup)
                    cnpj = data['cnpj']
                    emails = self._extract_email(soup)
                    cnaes = self._extract_cnaes(soup)
                    cnaes_with_comma = ', '.join(cnaes)

                    #====================================
                    
                    # Columns names
                    infos = ['CNPJ', 'NOME', 'CNAES', 'EMAILS']
                    values: List[str|List] = [cnpj, 
                                              company_name, 
                                              cnaes_with_comma, 
                                              emails]
                    # Create a dictionary with the columns names as keys and the data extracted as values.
                    val: Dict[str, str|List] = {x:y for x,y in zip(infos, values)}

                    # Add the dict at the ext list
                    ext.append(val)

                    # If show results is true, the program will print the data extracted.
                    if data['sw_res']:
                        print(f'Query Nº {index}')
                        print(f'{Colors.BLUE}[+]{Colors.RESET} NOME : {Colors.BLUE}{company_name}{Colors.RESET}')
                        print(f'{Colors.RED}[+]{Colors.RESET} CNPJ : {Colors.RED}{cnpj}{Colors.RESET}', end='\n')
                        print(f'{Colors.PURPLE}[+]{Colors.RESET} CNAES :', end=' ')
                        for cnae in cnaes:
                            print(f'{Colors.PURPLE}{cnae}{Colors.RESET}', end=' ')
                        print(f'\n{Colors.PURPLE}[@]{Colors.RESET} EMAILS : {emails}', end=' ')
                        print('\n\n')
        except Exception as e:
            print('Exception occurred: ', e)

        # Use the ext dictionary to create a Dataframe.
        df = pd.DataFrame(ext, columns=[x for x in infos])
        return df
