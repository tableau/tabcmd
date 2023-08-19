import sys

from tabcmd.execution.tabcmd_controller import TabcmdController


def main():
    if sys.version_info < (3, 8):
        raise ImportError(
            "Tabcmd requires Python 3.8+ but you are on " + sys.version_info + " - please update your python version."
        )

    try:
        parser = TabcmdController.initialize()
        TabcmdController.run(parser)
    except KeyboardInterrupt as ke:
        print("Keyboard Interrupt: exiting")
        sys.exit(1)
    except Exception as e:
        if e.__traceback__:
            sys.stderr.writelines(
                [
                    "ERROR\n",
                    "Unhandled exception: {}\n".format(type(e).__name__),
                    f"at line {e.__traceback__.tb_lineno} of {__file__}: {e}\n",
                ]
            )
        sys.exit(1)


if __name__ == "__main__":
    main()
