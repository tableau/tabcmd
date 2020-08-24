import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import ExportParser


class ExportCommand:
    def __init__(self, args, url):
        self.args = args
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
        separated_list = url.split("/")                        # FIX THIS
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
                req_option = TSC.RequestOptions()
                req_option.filter.add(TSC.Filter("contentUrl",
                                                 TSC.RequestOptions.Operator.Equals,
                                                 workbook))
                matching_workbook, _ = server.workbooks.get(
                    req_option)
                workbook_from_list = matching_workbook[0]

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
                    req_option = TSC.RequestOptions()
                    req_option.filter.add(TSC.Filter("contentUrl",
                                                     TSC.RequestOptions.Operator.Equals,
                                                     view))
                    matching_view, _ = server.views.get(
                        req_option)
                    views_from_list = matching_view[0]

                    req_option_pdf = TSC.PDFRequestOptions(maxage=1)

                    server.views.populate_pdf(views_from_list,
                                                  req_option_pdf)
                    if self.args.filename is None:
                        file_name_with_path = '{}.pdf'.format(views_from_list.name)
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
                    req_option = TSC.RequestOptions()
                    req_option.filter.add(TSC.Filter("contentUrl",
                                                     TSC.RequestOptions.Operator.Equals,
                                                     view))
                    matching_view, _ = server.views.get(
                        req_option)
                    views_from_list = matching_view[0]

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
                    req_option = TSC.RequestOptions()
                    req_option.filter.add(TSC.Filter("contentUrl",
                                                     TSC.RequestOptions.Operator.Equals,
                                                     view))
                    matching_view, _ = server.views.get(
                        req_option)
                    views_from_list = matching_view[0]

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
        # if self.args.pdf or self.args.png -r self.args.csv:
