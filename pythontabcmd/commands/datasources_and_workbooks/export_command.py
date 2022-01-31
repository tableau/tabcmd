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
        self.logger = log('pythontabcmd.export',
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

    def export(self, server):
        """Method to export using Tableauserverclient methods"""
        if self.args.fullpdf:  # its a workbook
            workbook = self.get_workbook(self.url)
            try:
                workbook_from_list = self.get_request_option_for_workbook(
                    server, workbook)

                req_option_pdf = TSC.PDFRequestOptions(maxage=1)

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
                self.logger.error("Server error occurred")

        if self.args.pdf or self.args.png or self.args.csv:  # its a workbook
            if self.args.pdf:  # its a view
                view = self.get_view(self.url)
                try:
                    views_from_list = self.get_request_option_for_view(
                        server, view)

                    req_option_pdf = TSC.PDFRequestOptions(maxage=1)

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
                    self.logger.error("Server error occurred")
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
                    self.logger.error("Server error occurred")
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
                    self.logger.error("Server error occurred")
