import sys
from setuptools import setup, find_packages

# Only install pytest and runner when test command is run
# This makes work easier for offline installs or low bandwidth machines
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_requirements = ['black','mock', 'pytest', 'pytest-cov', 'requests-mock>=1.0,<2.0', 'pyinstaller']

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
        'requests>=2.11,<3.0',
        'setuptools>=24.3',
        'tableauserverclient>=0.12',
        'urllib3>=1.24.3,<2.0',
    ],
    python_requires='>=3.6',
    setup_requires=pytest_runner,
    tests_require=test_requirements,
)
