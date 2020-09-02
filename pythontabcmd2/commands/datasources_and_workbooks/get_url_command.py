import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import GetUrlParser
import sys


class GetUrl:
    def __init__(self, args, url):
        self.url = url
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.get_url_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, url = GetUrlParser.get_url_parser()
        return cls(args, url)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.get_url(server_object)

    def evaluate_file_name(self, file_name, url):
        type_of_file = None
        if self.args.filename is not None:
            split_file_name = self.args.filename.split('.')
            type_of_file = split_file_name[1]
        elif self.args.filename is None:
            # grab from url
            split_url_to_get_extension = url.split('.')
            if len(split_url_to_get_extension) > 1:
                type_of_file = split_url_to_get_extension[1]
            else:
                print("Please include file extension")
                sys.exit()
        return type_of_file

    def get_workbook(self, url):
        # check the size of list
        separated_list = url.split("/")
        reversed_list = separated_list[::-1]
        return reversed_list[1]

    def check_if_extension_present(self, view):
        split_view = view.split(".")
        print(split_view, "check if extension")
        if len(split_view) == 2:    # Edge case cheCK
            print(split_view[1])
            if split_view[1] == "pdf" or split_view[1] == "csv" or \
                    split_view[1] == "png" or split_view[1] == "twb" or \
                    split_view[1] == "twbx" :  # add
                # workbook
                return True
            else:
                return False
        return False

    def get_view_without_extension(self, view):
        split_view = view.split(".")
        print("view withouy ext", split_view)
        return split_view[0]

    def get_workbook(self, url):
        separated_list = url.split("/")
        print("separated list get view", separated_list,
              separated_list[::-1][0])
        if self.check_if_extension_present(separated_list[::-1][0]):
            view_second_half_url = self.get_view_without_extension(
                separated_list[::-1][0])
            print("second half", view_second_half_url)
        else:
            view_second_half_url = separated_list[2]
            print(separated_list[2])
        return view_second_half_url

    def get_view(self, url):
        # check the size of list
        separated_list = url.split("/")
        print("separated list get view", separated_list,
              separated_list[::-1][0])
        if self.check_if_extension_present(separated_list[::-1][0]):
            view_second_half_url = self.get_view_without_extension(
                separated_list[::-1][0])
            print("second half", view_second_half_url)
        else:
            view_second_half_url = separated_list[2]
            print(separated_list[2])

        return '{}/sheets/{}'.format(separated_list[1], view_second_half_url)

    def get_url(self, server):
        """Method to get url using Tableauserverclient methods"""
        file_name = self.evaluate_file_name(self.args.filename, self.url)
        print(file_name)
        if file_name == "pdf":
            self.generate_pdf(server)
        elif file_name == "png":
            self.generate_png(server)
        elif file_name == "csv":
            self.generate_csv(server)
        elif file_name == "twbx" or file_name == "twb":
            self.generate_twb(server)
        else:
            print("Error file extension not found")
            sys.exit()

    def generate_pdf(self, server):
        view = self.get_view(self.url)
        print(view)
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter("contentUrl",
                                             TSC.RequestOptions.
                                             Operator.Equals,
                                             view))
            matching_view, _ = server.views.get(
                req_option)
            print(matching_view)
            views_from_list = matching_view[0]

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

    def generate_png(self, server):
        view = self.get_view(self.url)
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter("contentUrl",
                                             TSC.RequestOptions.
                                             Operator.Equals,
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

    def generate_csv(self, server):
        view = self.get_view(self.url)
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter("contentUrl",
                                             TSC.RequestOptions.
                                             Operator.Equals,
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

    def generate_twb(self, server):
        workbook = self.get_workbook(self.url)
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                             TSC.RequestOptions.
                                             Operator.Equals,
                                             workbook))
            matching_workbook, _ = server.workbooks.get(
                req_option)
            workbook_from_list = matching_workbook[0]

            server.workbooks.download(workbook_from_list.id, filepath=None,
                                      no_extract=False)
            self.logger.info("Workbook {} exported".format(
                workbook_from_list.name))
        except IndexError:
            self.logger.error("Please check if workbook is present")

        except TSC.ServerResponseError as e:
            self.logger.error("Server error occurred")
