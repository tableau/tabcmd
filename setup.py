try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pythontabcmd2',
    url='https://github.com/tableau/tabcmd2',
    packages=['pythontabcmd2', 'pythontabcmd2.commands', 'pythontabcmd2.parsers',
              'pythontabcmd2.tableauserverclient'],
    test_suite='Tests',
    install_requires=[
        'requests>=2.11,<3.0',
        'urllib3>=1.24.3,<2.0',
        'dill>=0.3'
    ],
    tests_require=[
        'requests-mock>=1.0,<2.0',
        'pytest',
        'mock',
        'unittests'
    ]
)