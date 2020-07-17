try:
    from .parser_invoker import *
    print("relative import works")
except ModuleNotFoundError:
    from parser_invoker import *
    print("absoulte import works")


class Tabcmd:
    def main(self):
        """Main method to call ParserInvoker class"""
        ParserInvoker()


if __name__ == '__main__':
    main_object = Tabcmd()
    main_object.main()
