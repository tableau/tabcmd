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
    package_data={'': ['res', 'src/locales']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tabcmd = src.tabcmd:main'
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
            'pyinstaller_versionfile',
            'setuptools_scm',
            'types-appdirs',
            'types-mock',
            'types-requests',
        ],
        'package': [
            'pyinstaller>=5.1',
            'pyinstaller-versionfile',
        ],
        'test': [
            'mock',
            'pytest', 'pytest-cov', 'pytest-order', 'pytest-runner',
            'requests-mock>=1.0,<2.0',
        ]
    },
    use_scm_version={
        "write_to": "src/execution/_version.py",
        "local_scheme": "no-local-version"  # require pypi supported versions always
    },
    zip_safe=False,
)
