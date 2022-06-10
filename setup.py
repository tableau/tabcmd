from setuptools import setup, find_packages


setup(
    name='tabcmd',
    author='Tableau',
    author_email='github@tableau.com',
    description='A command line client for working with Tableau Server.',
    license='MIT',
    url='https://github.com/tableau/tabcmd',

    python_requires='>=3.7',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tabcmd = tabcmd.tabcmd:main'
        ]
    },
    install_requires=[
        'polling2',
        'requests>=2.11,<3.0',
        'setuptools>=45',
        'tableauserverclient>=0.19',
        'urllib3>=1.24.3,<2.0',
    ],
    test_suite='tests',
    extras_require={
        'build': [
            'appdirs',
            'black',
            'mypy',
            'setuptools_scm',
        ],
        'package': [
            'pyinstaller>=5.1',
            'pyinstaller-versionfile',
        ],
        'test': [
            'mock',
            'pytest', 'pytest-cov', 'pytest-order', 'pytest-runner',
            'requests-mock>=1.0,<2.0',
            'types-appdirs',
            'types-mock',
            'types-requests',
        ]
    },
    use_scm_version={
        "write_to": "tabcmd/execution/_version.py",
    },
    zip_safe=False,
)
