class DecryptExtractsParser:
    """
    Parser for the command decryptextracts
    """

    @staticmethod
    def decrypt_extracts_parser(manager, command):
        """Method to parse decrypt extracts arguments passed by the user"""
        decrypt_extract_parser = manager.include(command)
        # TODO this argument is supposed to be optional - if not specified, do the default site
        decrypt_extract_parser.add_argument("site_name", metavar="site-name", help="name of site")
