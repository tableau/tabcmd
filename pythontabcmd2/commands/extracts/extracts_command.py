from ..commands import Commands


class ExtractsCommand(Commands):
    """
    Base class for extracts group of commands
    """
    def __init__(self, args):
        super().__init__(args)
