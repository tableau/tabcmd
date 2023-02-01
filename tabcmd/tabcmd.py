import sys

from tabcmd.execution.tabcmd_controller import TabcmdController


def main():

    if sys.version_info < (3, 7):
        raise ImportError(
            "Tabcmd requires Python 3.7 but you are on " + sys.version_info + " - please update your python version."
        )

    try:
        parser = TabcmdController.initialize()
        TabcmdController.run(parser)
    except KeyboardInterrupt as ke:
        print("Keyboard Interrupt: exiting")
        sys.exit(1)
    except Exception as e:
        sys.stderr.writelines(["ERROR\n", "Unhandled exception: {}\n".format(type(e).__name__),
            f"at line {e.__traceback__.tb_lineno} of {__file__}: {e}\n"]
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
