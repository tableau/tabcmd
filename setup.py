try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='tabcmd',
    url='https://github.com/tableau/tabcmd',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tabcmd = tabcmd.tabcmd:main'
        ]
    },
    test_suite='tests',
    install_requires=[
        'requests>=2.11,<3.0',
        'urllib3>=1.24.3,<2.0',
        'tableauserverclient>=0.12'
    ],
    tests_require=[
        'requests-mock>=1.0,<2.0',
        'pytest',
        'mock'
    ]
)