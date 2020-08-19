import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import ExportParser


class Export:
    def __init__(self, args):
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.export',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args = ExportParser.export_parser()
        return cls(args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.export(server_object)

    def get_workbook(self, url):
        # check the size of list
        separated_list = url.split("/")
        return separated_list[0]

    def export(self, server):
        """Method to export using Tableauserverclient methods"""

        if self.args.fullpdf:    # its workbook
            url = self.get_workbook(self.args.url)
            try:
                req_option = TSC.RequestOptions()
                req_option.filter.add(TSC.Filter("contentUrl",
                                                 TSC.RequestOptions.Operator.Equals,
                                                 url))
                matching_workbook, _ = server.workbooks.get(
                    req_option)
                workbook_from_list = matching_workbook[0]

                req_option_pdf = TSC.PDFRequestOptions(maxage=1)

                server.workbooks.populate_pdf(workbook_from_list,
                                              req_option_pdf)
                with open('./workbook_pdf.pdf', 'wb') as f:
                    f.write(workbook_from_list.pdf)

            except TSC.ServerResponseError as e:
                 self.logger.error("Server error occurred")






        # if self.args.pdf or self.args.png -r self.args.csv: