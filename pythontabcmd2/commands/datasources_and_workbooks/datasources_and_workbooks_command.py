from ..commands import Commands


class DatasourcesAndWorkbooks(Commands):
    def __init__(self, args):
        super().__init__(args)
        self.args = args
