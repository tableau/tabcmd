import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

# Only install pytest and runner when test command is run
# This makes work easier for offline installs or low bandwidth machines
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_requirements = ['mock', 'pycodestyle', 'pytest', 'requests-mock>=1.0,<2.0', 'pyinstaller']

setup(
    name='tabcmd',
    author='Tableau',
    author_email='github@tableau.com',
    url='https://github.com/tableau/tabcmd',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tabcmd = tabcmd.tabcmd:main'
        ]
    },
    description='A command line client for working with Tableau Server.',
    test_suite='tests',
    setup_requires=pytest_runner,
    install_requires=[
        'requests>=2.11,<3.0',
        'urllib3>=1.24.3,<2.0',
        'tableauserverclient>=0.12'
    ],
    tests_require=test_requirements,
    extras_require={
        'test': test_requirements
    }

)