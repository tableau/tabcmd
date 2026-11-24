import sys

try:
    from tabcmd.tabcmd import main
except Exception as e:
    ctx = ", caused by: {}".format(e.__context__) if e.__context__ else ""
    print("Exception thrown importing tabcmd: {}{}".format(e, ctx), file=sys.stderr)
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        print("Application is running in an executable bundle", file=sys.stderr)
        print("sys.argv[0] is", sys.argv[0], file=sys.stderr)
        print("sys.executable is", sys.executable, file=sys.stderr)
    else:
        print(
            "[Possible cause: tabcmd is installed but broken, try `pip install --force-reinstall tabcmd`]",
            file=sys.stderr,
        )
    sys.exit(1)


if __name__ == "__main__":
    main()
