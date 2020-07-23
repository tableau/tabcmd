try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='pythontabcmd2',
    url='https://github.com/tableau/tabcmd2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tabcmd2 = pythontabcmd2.tabcmd2:main'
        ]
    },
    test_suite='tests',
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