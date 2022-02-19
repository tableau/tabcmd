
Developer Readme

- build
> python setup.py build

- run tests:
> pytest

- style is enforced with pycodestyle, mostly using default settings. https://www.mankier.com/1/pycodestyle
> pycodestyle tabcmd tests

- packaging is done with pyinstaller, using github actions for cross-platform setup
> pyinstaller tabcmd/tabcmd.py --clean --noconfirm

produces dist/tabcmd.exe
> dist/tabcmd/tabcmd.exe --help
> 