try:
    from .parser_invoker import *
except ImportError:
    from parser_invoker import *


class Tabcmd:
    def main(self):
        """Main method to call ParserInvoker class"""
        ParserInvoker()


if __name__ == '__main__':
    main_object = Tabcmd()
    main_object.main()
