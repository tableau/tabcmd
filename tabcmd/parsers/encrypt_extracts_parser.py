class EncryptExtractsParser:
    """
    Parser for the command encryptextracts
    """

    @staticmethod
    def encrypt_extracts_parser(manager, command):
        """Method to parse encrypt extracts arguments passed by the user"""
        encrypt_extract_parser = manager.include(command)
        encrypt_extract_parser.add_argument('sitename', help='name of site')
