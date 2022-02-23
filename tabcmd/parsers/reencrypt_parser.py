import sys


class ReencryptExtractsParser:
    """
    Parser to reencrypt command
    """

    @staticmethod
    def reencrypt_extracts_parser(manager, command):
        """Method to parse reencrypt extracts arguments passed by the user"""
        reencrypt_extract_parser = manager.include(command)
        reencrypt_extract_parser.add_argument(
         'sitename', help='The site to encrypt extracts for')
