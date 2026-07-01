import sys

try:
    from tabcmd.tabcmd import main
except ImportError as e:
    print(
        "Exception thrown importing tabcmd: `{}`, `{}`".format(e, e.__context__),
        file=sys.stderr,
    )
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        print("Application is running in an executable bundle")
        print("sys.argv[0] is", sys.argv[0])
        print("sys.executable is", sys.executable)
    else:
        print(
            "[Possible cause: Tabcmd needs to be installed, try `pip install tabcmd`]",
            file=sys.stderr,
        )
    sys.exit(1)

main()
