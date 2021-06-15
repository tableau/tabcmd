import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import ExportParser
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class ExportCommand(DatasourcesAndWorkbooks):
    """
    Command to Export a view or workbook from Tableau Server and save
    it to a file. This command can also export just the data used for a view
    """
    def __init__(self, args, url):
        super().__init__(args)
        self.url = url
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.export',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, url = ExportParser.export_parser()
        return cls(args, url)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.export(server_object)

    def get_workbook(self, url):
        # check the size of list
        separated_list = url.split("/")
        reversed_list = separated_list[::-1]
        return reversed_list[1]

    def get_view(self, url):
        # check the size of list
        separated_list = url.split("/")
        if len(separated_list) > 2:
            print("error")
        return '{}/sheets/{}'.format(separated_list[0], separated_list[1])

    def get_pdf_request_options(self):
        # handle orientation and page type options
        req_option_pdf = TSC.PDFRequestOptions(maxage=1)
        if self.args.pagelayout == 'landscape':
            req_option_pdf.orientation =
                TSC.PDFRequestOptions.Orientation.Landscape
        else:
            req_option_pdf.orientation =
                TSC.PDFRequestOptions.Orientation.Portrait

        if self.args.pagesize == 'a3':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.A3
        elif self.args.pagesize == 'a4':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.A4
        elif self.args.pagesize == 'a5':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.A5
        elif self.args.pagesize == 'b5':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.B5
        elif self.args.pagesize == 'executive':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.Executive
        elif self.args.pagesize == 'folio':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.Folio
        elif self.args.pagesize == 'ledger':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.Ledger
        elif self.args.pagesize == 'legal':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.Legal
        elif self.args.pagesize == 'note':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.Note
        elif self.args.pagesize == 'quarto':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.Quarto
        elif self.args.pagesize == 'tabloid':
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.Tabloid
        else:
            req_option_pdf.page_type = TSC.PDFRequestOptions.PageType.Letter
        return req_option_pdf

    def export(self, server):
        """Method to export using Tableauserverclient methods"""
        if self.args.fullpdf:  # its a workbook
            workbook = self.get_workbook(self.url)
            try:
                workbook_from_list = self.get_request_option_for_workbook(
                    server, workbook)
                req_option_pdf = self.get_pdf_request_options()
                server.workbooks.populate_pdf(workbook_from_list,
                                              req_option_pdf)
                if self.args.filename is None:
                    file_name_with_path = '{}.pdf'.format(workbook)
                else:
                    file_name_with_path = self.args.filename
                formatted_file_name = file_name_with_path
                with open(formatted_file_name, 'wb') as f:
                    f.write(workbook_from_list.pdf)
                    self.logger.info("Exported successfully")

            except TSC.ServerResponseError as e:
                self.logger.error("Server error occurred: {}".format(e))

        if self.args.pdf or self.args.png or self.args.csv:  # its a workbook
            if self.args.pdf:  # its a view
                view = self.get_view(self.url)
                try:
                    views_from_list = self.get_request_option_for_view(
                        server, view)

                    req_option_pdf = self.get_pdf_request_options()

                    server.views.populate_pdf(views_from_list,
                                              req_option_pdf)
                    if self.args.filename is None:
                        file_name_with_path = '{}.pdf'.format(views_from_list.
                                                              name)
                    else:
                        file_name_with_path = self.args.filename
                    formatted_file_name = file_name_with_path
                    with open(formatted_file_name, 'wb') as f:
                        f.write(views_from_list.pdf)
                        self.logger.info("Exported successfully")

                except TSC.ServerResponseError as e:
                    self.logger.error("Server error occurred: {}".format(e))
            if self.args.csv:
                view = self.get_view(self.url)
                try:
                    views_from_list = self.get_request_option_for_view(
                        server, view)

                    req_option_csv = TSC.CSVRequestOptions(maxage=1)

                    server.views.populate_csv(views_from_list,
                                              req_option_csv)
                    if self.args.filename is None:
                        file_name_with_path = '{}.csv'.format(view)
                    else:
                        file_name_with_path = self.args.filename
                    formatted_file_name = file_name_with_path
                    with open(formatted_file_name, 'wb') as f:
                        f.write(views_from_list.csv)
                        self.logger.info("Exported successfully")

                except TSC.ServerResponseError as e:
                    self.logger.error("Server error occurred: {}".format(e))
            if self.args.png:
                view = self.get_view(self.url)
                try:
                    views_from_list = self.get_request_option_for_view(
                        server, view)
                    req_option_csv = TSC.CSVRequestOptions(maxage=1)
                    server.views.populate_csv(views_from_list,
                                              req_option_csv)
                    if self.args.filename is None:
                        file_name_with_path = '{}.png'.format(view)
                    else:
                        file_name_with_path = self.args.filename
                    formatted_file_name = file_name_with_path
                    with open(formatted_file_name, 'wb') as f:
                        f.write(views_from_list.png)
                        self.logger.info("Exported successfully")

                except TSC.ServerResponseError as e:
                    self.logger.error("Server error occurred: {}".format(e))
