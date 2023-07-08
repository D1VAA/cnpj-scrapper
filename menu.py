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
        self.title = f'{title}' if title is not None else t
        self.menu_o = {'help': self._show_help, 'config': self.handle_params}
        self.opt = dict()
        print(f'\n\n{Colors.YELLOW}[+]{Colors.RESET} Starting console...')
        print(self.title, end='\n\n')

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
        print(f'{"=" * 25} COMANDOS {"=" * 25}', end='\n\n')
        print(
            f'{Colors.CIAN}[*] help  {Colors.YELLOW} >{Colors.RESET} Descrição da função.')
        print(
            f'{Colors.CIAN}[*] config {Colors.YELLOW}>{Colors.RESET} Ajusta os parâmetros da função')
        print(f'{Colors.CIAN}[*] run   {Colors.YELLOW} >{Colors.RESET} Executar a função.')
        print(f'{Colors.CIAN}[*] exit  {Colors.YELLOW} >{Colors.RESET} Sai do console.', end='\n\n')

        print(f'{"=" * 25} FUNÇÕES {"=" * 25}', end='\n\n')
        for option, values in self.opt.items():
            if isinstance(values, list):
                v = ','.join(values)
            else:
                func_name = values.__name__
                v = f'Run: {Colors.CIAN}{func_name}{Colors.RESET}'
            print(f'{Colors.YELLOW}[+] {option:<6}{Colors.YELLOW} > {Colors.RESET}{v}', end='\n')
        self._menu()

    def _show_help(self, inp):
        func = self.opt[inp]
        func_path = inspect.getfile(func)
        func_name = func.__name__
        v = f'{Colors.CIAN}{func_name}{Colors.RESET}'
        m = 12  # Margin

        print('\n\n')
        print(f'{Colors.YELLOW}[-] {inp:<6}{Colors.YELLOW} > {Colors.RESET}{v}', end='\n')
        print(f'{" " * m}{Colors.RED}|[DESCRIÇÃO]{Colors.RESET}')

        for x in func.__doc__.splitlines():
            print(f'{" " * m}{Colors.RED}|{Colors.RESET}{x}')
        print(f'{" " * m}{Colors.RED}|>{Colors.RESET}{Colors.CIAN}{func_path}{Colors.RESET}')
        self._menu()

    def handle_params(self, module):
        func = self.opt[module]
        sig = inspect.signature(self.opt[module])
        params = sig.parameters
        print('[*] help [PARAM_NAME] > Para mais informações do parâmetro')
        print("[*] set [PARAM_NAME] > Para configurar o valor do parâmetro.")
        print(params)

    def _handle_func(self, cmd, func):
        sig = inspect.signature(self.opt[func])
        self.menu_o[cmd](func)

    def _menu(self):
        print('\n')
        while True:
            try:
                inp = list(str(input(f'\r{Colors.RED}>{Colors.RESET} ')).split())
                func = inp[-1]  # Nome da função
                command = ''.join(inp[:-1]) if len(inp) >= 2 else func  # Comando

                if func in ['exit', 'quit']:
                    print(f'{Colors.RED}[-]{Colors.RESET} Encerrando console...')
                    break

                elif command in self.menu_o.keys() and func in self.opt.keys():
                    self._handle_func(command, func)

                else:
                    print('\rTodos os parâmetros precisam ser fornecidos\n\n')

            except KeyboardInterrupt:
                print("\r'exit' para encerrar o console.")
        return

    def run(self):
        self._show_menu_options()
