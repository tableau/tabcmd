import sys
from setuptools import setup, find_packages

# Only install pytest and runner when test command is run
# This makes work easier for offline installs or low bandwidth machines
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
test_requirements = ['appdirs',
                     # 'bumpversion',
                     'black',
                     'mock',
                     'pyinstaller>=5.1',
                     'pytest', 'pytest-cov', 'pytest-order', 'pytest-runner',
                     'requests-mock>=1.0,<2.0']

setup(
    name='tabcmd',
    author='Tableau',
    author_email='github@tableau.com',
    description='A command line client for working with Tableau Server.',
    entry_points={
        'console_scripts': [
            'tabcmd = tabcmd.tabcmd:main'
        ]
    },
    license='MIT',
    packages=find_packages(),
    test_suite='tests',
    url='https://github.com/tableau/tabcmd',
    extras_require={
        'test': test_requirements,
        'package': ['pyinstaller>=4.8']
    },
    install_requires=[
        'types-appdirs',
        'polling2',
        'requests>=2.11,<3.0',
        'setuptools>=45',
        'setuptools_scm',
        'tableauserverclient>=0.19',
        'types-mock',
        'types-requests',
        'urllib3>=1.24.3,<2.0',
    ],
    python_requires='>=3.7',
    tests_require=test_requirements,
    use_scm_version={
        "write_to": "_version.py",
    },
    setup_requires=['setuptools_scm'],
)
