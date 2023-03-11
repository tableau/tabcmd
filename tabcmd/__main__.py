import sys

try:
    from tabcmd.tabcmd import main
except ImportError as e:
    print("Exception thrown running program: `{}`, `{}`".format(e, e.__context__), file=sys.stderr)
    print("[Possible cause: Tabcmd needs to be run as a module, try running `python -m tabcmd`]", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()
