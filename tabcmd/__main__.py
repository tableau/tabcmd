import sys

try:
    from tabcmd.tabcmd import main
except ImportError:
    print("Tabcmd needs to be run as a module, it cannot be run as a script")
    print("Try running python -m tabcmd")
    sys.exit(1)

if __name__ == "__main__":
    main()
