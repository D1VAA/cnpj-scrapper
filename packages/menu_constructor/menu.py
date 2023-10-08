import inspect
from packages.bcolors import Colors
from time import sleep

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
        self.menu_o = {'menu': self._show_menu_options,
                       'help': self._show_help,
                       'config': self._handle_params,
                       'run': self._execute_func}
        self.opt = dict()
        self.params_funcs = dict()
        self.executions = dict()
        print(f'\n\n{Colors.YELLOW}[+]{Colors.RESET} Starting console...')
        sleep(1)
        print(self.title, end='\n\n')

    def add_option(self, opt_title, func=None):
        """
        Simple menu option creator
        :param opt_title: the option name
        :param func: used if the option shoul return a function
        """
        self.opt[opt_title] = func

        # Extracting the parameters and function name
        sig = inspect.signature(func)
        params = sig.parameters
        func_name = func.__name__
        self.params_funcs[func_name] = {}
        for name, param in params.items():
            # Set 'No default value' if parameter has no default value
            value = param.default if param.default != inspect._empty else 'No Default Value'
            self.params_funcs[func_name][name] = value

    # Method with series of print statements to show the menu options
    def _show_menu_options(self, func_name=None, caller_name=None):
        print('\n\n')
        if caller_name == '_menu':
            print(f'{"=" * 25} COMANDOS {"=" * 25}', end='\n\n')
            print(f'{Colors.CIAN}[*] menu  {Colors.YELLOW} >{Colors.RESET} Mostra esse menu')
            print(
                f'{Colors.CIAN}[*] help  {Colors.YELLOW} >{Colors.RESET} Descrição da função.')
            print(
                f'{Colors.CIAN}[*] config {Colors.YELLOW}>{Colors.RESET} Ajusta os parâmetros da função')
            print(f'{Colors.CIAN}[*] run   {Colors.YELLOW} >{Colors.RESET} Executa a função.')
            print(f'{Colors.CIAN}[*] exit  {Colors.YELLOW} >{Colors.RESET} Sai do console.', end='\n\n')

            print(f'{"=" * 25} FUNÇÕES {"=" * 25}', end='\n\n')
            for option, values in self.opt.items():
                func_name = values.__name__
                v = f'Executa: {Colors.BLUE}{func_name}{Colors.RESET}'
                print(f'{Colors.YELLOW}[+] {option:<6}{Colors.YELLOW} > {Colors.RESET}{v}', end='\n')
            print('\n\n')
        elif caller_name == '_handle_params' and func_name is not None:
            m = max(len(func_name) + 2, len('[FUNÇÃO]'))

            print(f'{"=" * 25} COMANDOS {"=" * 25}', end='\n\n')
            print(f'{Colors.CIAN}[*] menu {Colors.YELLOW} >{Colors.RESET} Mostra esse menu.')
            print(f'{Colors.CIAN}[*] help {Colors.YELLOW} >{Colors.RESET} Para mais informações do parâmetro')
            print(f"{Colors.CIAN}[*] set   {Colors.YELLOW}>{Colors.RESET} Definir valor para o parâmetro.",
                  end='\n\n')
            print(f'{"=" * 24} PARÂMETROS {"=" * 24}', end='\n\n')
            print(
                f'{Colors.BLUE}[FUNÇÃO]{Colors.RESET}{Colors.YELLOW}{" " * (m - len("[FUNÇÃO]"))}|   [PARAMETROS]\n{" " * m}|{Colors.RESET}',
                end='\n')
            print(f'{Colors.BLUE}>{func_name}{Colors.YELLOW}{" " * (m - len(func_name) - 1)}|{Colors.RESET}')
            for name, parameters in self.params_funcs[func_name].items():
                print(f'{" " * m}{Colors.YELLOW}|   {name:<15} > {parameters}{Colors.RESET}')
            print(f'{" " * m}{Colors.YELLOW}|{Colors.RESET}\n\n')

    # Method called when 'help' is used
    def _show_help(self, func, param=None):
        print('\n\n')
        # Condition called when config menu use help
        if param is not None:
            # Extract the parameter annotations
            sig = inspect.signature(func)
            p = sig.parameters[param].annotation
            param_desc = p if p is not inspect.Parameter.empty else '\tParâmetro não possui descrição disponível.\n'
            param_desc = param_desc.splitlines()
            m = max(len(param) + 2, 11)
            print(
                f'{Colors.CIAN}[PARAMETRO]{Colors.YELLOW}{" " * (m - len("[PARAMETRO]"))}|   [TYPE]\n{" " * m}|{Colors.RESET}',
                end='\n')
            print(f'{Colors.CIAN}>{param}{Colors.YELLOW}{" " * (m - len(param) - 1)}|')
            for x in param_desc:
                print(f'{" " * m}{Colors.YELLOW}|>{x}{Colors.RESET}')
            print(f'{" " * m}{Colors.YELLOW}|{Colors.RESET}\n\n')
        else:
            func_path = inspect.getfile(func)
            func_name = func.__name__
            v = f'{Colors.CIAN}>{func_name}{Colors.RESET} '
            m = max(len(func_name) + 2, 11)

            print(f'{v}{Colors.RED}|[DOCSTRING]{Colors.RESET}')
            docstring = func.__doc__ if func.__doc__ is not None else '\n\tSem descrição disponível para a função.\n\n'
            doc_lines = docstring.splitlines()

            for x in doc_lines:
                print(f'{" " * m}{Colors.RED}|{Colors.RESET}{x}')
            print(f'{" " * m}{Colors.RED}|[path]> {Colors.RESET}{Colors.CIAN}{func_path}{Colors.RESET}', '\n')

    # Method called to update the parameter value
    def _update_p_value(self, func, param, value):
        n_value = value
        func_name = func.__name__
        try:
            if '$' in value:
                value = value.replace('$', '')
                n_value = self.opt[value].__name__
                value = self.executions[n_value]
        except KeyError:
            print(
                f'\n\n{Colors.RED}[!]{Colors.RESET} Ocorreu um erro.\n\nVerifique:')
            print('- Se o nome da função está correto.')
            print('- Se ela já foi executada.')
            print('- Se ela está retornando algum valor que possa ser reutilizado.\n\n')
            return
        old_v = self.params_funcs[func_name][param]
        self.params_funcs[func_name][param] = value
        print('\n\n')
        print(
            f"{Colors.CIAN}[UPDATE] {param} > {Colors.RED}|{old_v}| {Colors.RESET}-->{Colors.CIAN} |{n_value}|{Colors.RESET}")
        print('\n\n')

    # Method called when config mode is activated
    def _handle_params(self, func):
        func_name = func.__name__

        # No parameter to be configured
        if len(self.params_funcs[func_name].items()) < 1:
            print('\n\n')
            print(f'{Colors.RED}[!]{Colors.RESET} A função não possui parâmetros a serem configurados.')
            print('\n\n')
            return

        self._show_menu_options(func_name, '_handle_params')
        cmds = {'help': self._show_help,
                'set': self._update_p_value,
                'menu': self._show_menu_options}
        while True:
            try:
                cmd = input(f'{Colors.PURPLE}config>{Colors.RESET} ')
                inp = list(str(cmd).split())
                args = [func]
                cmd = inp[0]
                if cmd in ['exit', 'quit', 'back']:
                    print(f'\n{Colors.PURPLE}[↲]{Colors.RESET} Retornando...\n\n')
                    return

                elif cmd in cmds.keys():
                    args.append(inp[1:][0]) if len(inp) > 1 else None
                    if cmd == 'menu':
                        args[0] = func_name
                        args.append('_handle_params')
                    elif cmd == 'set':
                        args.append(' '.join(inp[2:]))
                    cmds[cmd](*args)

                elif cmd not in cmds and len(cmd) > 0:
                    print(f"\n\n{Colors.RED}[?]{Colors.RESET} Comando inválido...\n\n")

            except KeyboardInterrupt:
                print(f"\n\n{Colors.RED}[!]{Colors.RESET} Digite 'exit' para sair...\n\n")
            except KeyError as e:
                print(f"\n\n{Colors.RED}[!]{Colors.RESET} Opção {e} não é válida!\n\n")

    def _execute_func(self, func):
        func_name = func.__name__
        params_func = self.params_funcs[func_name]

        if bool(self.params_funcs[func_name]) and 'No Default Value' not in params_func.values():
            print(f"\n\n{Colors.PURPLE}[-]{Colors.RESET} Executando...\n\n")
            sleep(0.4)
            e = func(**params_func)
            print(f"\n\n{Colors.GREEN}[✓]{Colors.RESET} Execução finalizada!\n\n")

        elif not bool(self.params_funcs[func_name]):
            print(f"\n\n{Colors.PURPLE}[-]{Colors.RESET} Executando...\n\n")
            sleep(0.4)
            e = func()
            print(f"\n\n{Colors.GREEN}[✓]{Colors.RESET} Execução finalizada!\n\n")

        else:
            print(f'\n\n{Colors.RED}[!]{Colors.RESET} Necessário configurar os parâmetros da função.\n\n')
            return
        self.executions[func_name] = e

    def _menu(self):
        self._show_menu_options(caller_name='_menu')
        while True:
            try:
                cmd = input(f'{Colors.RED}>{Colors.RESET} ')
                inp = list(str(cmd).split())
                func_name = inp[-1]  # Nome da função
                command = ''.join(inp[:-1]) if len(inp) >= 2 else func_name  # Comando

                if command in ['exit', 'quit']:
                    print(f'\n\n{Colors.RED}[-]{Colors.RESET} Encerrando console...')
                    return

                elif command == 'menu':
                    self.menu_o[command](caller_name='_menu')

                elif command in self.menu_o.keys() and func_name in self.opt.keys():
                    self.menu_o[command](self.opt[func_name])

                elif command in self.menu_o.keys() and func_name not in self.opt.keys():
                    print(f'\n\n{Colors.RED}[!]{Colors.RESET} Algum parâmetro está incorreto ou faltando.\n\n')
                else:
                    print(f'\n\n{Colors.RED}[?]{Colors.RESET} Comanda Inválido\n\n')

            except KeyboardInterrupt:
                print(f"\n\n{Colors.RED}[!]{Colors.RESET} Digite 'exit' para encerrar o console.\n\n")

            except (TypeError, IndexError):
                pass
