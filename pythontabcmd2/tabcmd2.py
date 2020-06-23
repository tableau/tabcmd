try:
    from parser_invoker import *
except ImportError:
    from .parser_invoker import *


class Tabcmd:


    def main(self):
        ParserInvoker()

if __name__ == '__main__':
    main_object = Tabcmd()
    main_object.main()
