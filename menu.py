import inspect
from packages.bcolors import Colors

t = '''
--    /$$$$$$                                 /$$$$$$                                                                      
--   /$$__  $$                               /$$__  $$                                                                     
--  | $$  \__/ /$$$$$$$   /$$$$$$  /$$      | $$  \__/  /$$$$$$$  /$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
--  | $$      | $$__  $$ /$$__  $$|__/      |  $$$$$$  /$$_____/ /$$__  $$|____  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$
--  | $$      | $$  \ $$| $$  \ $$ /$$       \____  $$| $$      | $$  \__/ /$$$$$$$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/
--  | $$    $$| $$  | $$| $$  | $$| $$       /$$  \ $$| $$      | $$      /$$__  $$| $$  | $$| $$  | $$| $$_____/| $$      
--  |  $$$$$$/| $$  | $$| $$$$$$$/| $$      |  $$$$$$/|  $$$$$$$| $$     |  $$$$$$$| $$$$$$$/| $$$$$$$/|  $$$$$$$| $$      
--   \______/ |__/  |__/| $$____/ | $$       \______/  \_______/|__/      \_______/| $$____/ | $$____/  \_______/|__/      
--                      | $$ /$$  | $$                                             | $$      | $$                          
--                      | $$|  $$$$$$/                                             | $$      | $$                          
--                      |__/ \______/                                              |__/      |__/                          
'''


class MenuConstructor:
    def __init__(self, title=None):
        pass
        self.title = f'{title}' if title is not None else t
        self.help_m = ''
        self.opt = dict()

    def add_option(self, opt_title, opts: list = None, attr=None):
        """
        Simple menu option creator
        :param attr: used if the option shoul return a function
        :param opt_title: for name the option
        :param opts: list that contain the valid options
        """
        opt = opts if opts is not None else attr
        self.opt[opt_title] = opt

    def _show_menu_options(self):
        print('\n\n')
        print(f'{Colors.YELLOW}[+]{Colors.RESET} Starting console...')
        print(self.title, end='\n\n')
        print(f'{"=" * 25} OPÇÕES {"=" * 25}', end='\n\n')
        print(f'{Colors.CIAN}[*] help  {Colors.YELLOW} >{Colors.RESET} Mostra novamente o menu de opções.')
        print(f'{Colors.CIAN}[*] exit  {Colors.YELLOW} >{Colors.RESET} Sai do console.', end='\n\n')
        for option, values in self.opt.items():
            if isinstance(values, list):
                v = ','.join(values)
            else:
                func_name = values.__name__
                func_path = inspect.getfile(values)
                v = f'Executa: {Colors.CIAN }{func_name}{Colors.RESET}\
                \n{" "*21}{Colors.RED}|[DESCRIÇÃO]{Colors.RESET}'
                print(f'{Colors.YELLOW}[-] {option:<6}{Colors.YELLOW} > {Colors.RESET}{v}', end='\n')
                for x in values.__doc__.splitlines():
                    print(f'{" "*21}{Colors.RED}|{Colors.RESET}{x}')
                print(f'{" "*21}{Colors.RED}|>{Colors.RESET}{Colors.CIAN}{func_path}{Colors.RESET}')
        self._menu()

    def _menu(self):
        print('\n')
        try:
            while True:
                inp = str(input('> '))
                if inp == 'help':
                    self._show_menu_options()
                if inp == 'exit' or inp == 'quit':
                    break
                if inp in self.opt.keys():
                    self.opt[inp]()
        except KeyboardInterrupt:
            print("\rInterrupção pelo teclado. Use 'exit' para encerramento adequado.")
    
    def exec(self):
        self._show_menu_options()


def scrapper():
    """
    Texto aleatório para textar o print da descrição da função no terminal
    Deve aparecer linha por linha
    """
    print('Executa o scrapper')


menu = MenuConstructor()
menu.add_option('exec', attr=scrapper)
menu.exec()
