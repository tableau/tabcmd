import sys

from tabcmd.execution.tabcmd_controller import TabcmdController


def main():

    if sys.version_info < (3, 7):
        raise ImportError(
            "Tabcmd requires Python 3.7 but you are on " + sys.version_info + " - please update your python version."
        )

    try:
        print("Launching tabcmd")
        parser = TabcmdController.initialize()
        TabcmdController.run(parser)
    except Exception as any_exception:
        print("Unexpected error: {}".format(any_exception))
        sys.exit(1)


if __name__ == "__main__":
    main()
