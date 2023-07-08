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

def completer(text, state):
    options = [i for i in options if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

class MenuConstructor:
    def __init__(self, title=None):
        self.title = f'{title}' if title is not None else t
        self.menu_o = {'help': self._show_help, 'config': self._handle_params, 'run': self._execute_func}
        self.opt = dict()
        self.params_funcs = dict()
        print(f'\n\n{Colors.YELLOW}[+]{Colors.RESET} Starting console...')
        print(self.title, end='\n\n')

    def add_option(self, opt_title, opts: list = None, func=None):
        """
        Simple menu option creator
        :param attr: used if the option shoul return a function
        :param opt_title: for name the option
        :param opts: list that contain the valid options
        """
        self.opt[opt_title] = func

        # Extracting the parameters
        sig = inspect.signature(func)
        params = sig.parameters
        func_name = func.__name__
        self.params_funcs[func_name] = {}
        for name, param in params.items():
            # Set None if parameter has no default value
            value = param.default if param.default != inspect._empty else None
            self.params_funcs[func_name][name] = value


    def _show_menu_options(self, menu, func_name=None):
        print('\n\n')
        print(f'{"=" * 25} COMANDOS {"=" * 25}', end='\n\n')
        if menu == 'menu':
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
                    v = f'Executa: {Colors.BLUE}{func_name}{Colors.RESET}'
                print(f'{Colors.YELLOW}[+] {option:<6}{Colors.YELLOW} > {Colors.RESET}{v}', end='\n')
            print('\n\n')
            self._menu()
        elif menu == 'config':
            m = len(func_name) + 1
            print(f'{Colors.CIAN}[*] help {Colors.YELLOW} >{Colors.RESET} Para mais informações do parâmetro')
            print(f"{Colors.CIAN}[*] set   {Colors.YELLOW}>{Colors.RESET} Definir valor para o parâmetro.",end='\n\n')
            print(f'{"=" * 24} PARAMETROS {"=" * 24}', end='\n\n')
            print(f'{Colors.BLUE}[FUNÇÃO]{Colors.RESET}{Colors.YELLOW}{" "*6}|   [PARAMETROS]\n{" "*m}|{Colors.RESET}', end='\n')
            print(f'{Colors.BLUE}{func_name}{Colors.YELLOW} |{Colors.RESET}')
            for name, parameters in self.params_funcs[func_name].items():
                print(f'{" "*m}{Colors.YELLOW}|   {name:<15} >{Colors.CIAN} {parameters}{Colors.RESET}')
            print(f'{" "*m}{Colors.YELLOW}|{Colors.RESET}\n\n')

    def _show_help(self, func, param=None):
        if param is not None:
            sig = inspect.signature(func)
            p = sig.parameters[param].annotation
            param_desc = p if p is not inspect.Parameter.empty else 'Parâmetro não possui descrição disponível.'
            param_desc = param_desc.splitlines()
            m = max(len(param) + 2, 11)
            print(m)
            print(f'{Colors.PURPLE}[PARAMETRO]{Colors.YELLOW}{" "*(13-m)}|   [DESCRIÇÃO]\n{" "*m}|{Colors.RESET}', end='\n')
            print(f'{Colors.PURPLE}{param}{Colors.YELLOW}{" "*(m-len(param))}|')
            for x in param_desc:
                print(f'{" "*m}{Colors.YELLOW}|   {x}{Colors.RESET}')
            print(f'{" "*m}{Colors.YELLOW}|{Colors.RESET}\n\n')

        else:
            func_path = inspect.getfile(func)
            func_name = func.__name__
            v = f'{Colors.CIAN}{func_name}{Colors.RESET}'
            m = max(len(func_name) + 2, 11)

            print('\n')
            print(f'{Colors.YELLOW}>{Colors.RESET}{v}', end=' ')
            print(f'{Colors.RED}|[DESCRIÇÃO]{Colors.RESET}')

            for x in func.__doc__.splitlines():
                print(f'{" " * m}{Colors.RED}|{Colors.RESET}{x}')
            print(f'{" " * m}{Colors.RED}|>{Colors.RESET}{Colors.CIAN}{func_path}{Colors.RESET}', '\n')

    def _update_p_value(self, func, value):
        func_name = func.__name__
        self.params_funcs[func_name][param] = value

    def _handle_params(self, func):
        func_name = func.__name__
        self._show_menu_options('config', func_name)
        cmds = {'help': self._show_help, 'set': None}
        while True:
            try:
                cmd = input(f'{Colors.RED}config>{Colors.RESET} ')
                inp = list(str(cmd).split())
                args = list()
                cmd = inp[0] 
                value = inp[-1]
                param = inp[1:][0] if cmd != 'set' else value

                if cmd in ['exit', 'quit', 'back']:
                    print(f'\n{Colors.PURPLE}[-]{Colors.RESET} Retornando...\n\n')
                    return

                if cmd in cmds.keys():
                    cmds[cmd](func, param)

                elif cmd not in cmds and len(cmd) > 0:
                    print("Comando inválido...")

                else:
                    pass

            except KeyboardInterrupt:
                handle_params(func)
            except (TypeError, IndexError):
                pass

    def _execute_func(self, func):
        sig = inspect.signature(func)
        params = sig.parameters
        func_name = func.__name__
        if not bool(self.params_funcs[func_name]) and len(self.params_funcs[func_name]) == 0:
            func()
        else:
            print(f'Necessário configurar os parâmetros da função.')

    def _menu(self):
        while True:
            try:
                cmd = input(f'{Colors.RED}>{Colors.RESET} ')
                inp = list(str(cmd).split())
                func_name = inp[-1]  # Nome da função
                command = ''.join(inp[:-1]) if len(inp) >= 2 else func_name  # Comando

                if command in ['exit', 'quit']:
                    print(f'\n{Colors.RED}[-]{Colors.RESET} Encerrando console...')
                    return

                elif command in self.menu_o.keys() and func_name in self.opt.keys():
                    self.menu_o[command](self.opt[func_name])

                else:
                    print('\rTodos os parâmetros precisam ser fornecidos\n\n')

            except KeyboardInterrupt:
                print("\rDigite 'exit' para encerrar o console.")

            except (TypeError, IndexError):
                pass

    def run(self):
        self._show_menu_options('menu')
