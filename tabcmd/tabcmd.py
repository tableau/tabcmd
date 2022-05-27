import sys
import logging
from tabcmd.execution.tabcmd_controller import TabcmdController


def main():

    if sys.version_info < (3, 7):
        raise ImportError(
            "Tabcmd requires Python 3.7 but you are on " + sys.version_info + " - please update your python version."
        )

    try:
        parser = TabcmdController.initialize()
        TabcmdController.run(parser)
    except Exception as e:
        print("Unhandled exception: {}".format(type(e).__name__))
        print(
            f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
