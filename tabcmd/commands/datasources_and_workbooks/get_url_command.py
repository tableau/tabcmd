import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _


class GetUrl(DatasourcesAndWorkbooks):
    """
    This command gets the resource from Tableau Server that's represented
    by the specified (partial) URL. The result is returned as a file.
    """

    name: str = "get"
    description: str = _("get.short_description")

    @staticmethod
    def define_args(get_url_parser):
        get_url_parser.add_argument("url", help=_("get.errors.requires_url"))
        set_filename_arg(get_url_parser)
        # TODO add args for png size in pixels, refresh
        # to send to the server these are both just set on the url?

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        file_type = GetUrl.evaluate_file_name(logger, args.filename, args.url)
        if file_type == "pdf":
            GetUrl.generate_pdf(logger, server, args)
        elif file_type == "png":
            GetUrl.generate_png(logger, server, args)
        elif file_type == "csv":
            GetUrl.generate_csv(logger, server, args)
        elif file_type == "twbx" or file_type == "twb":
            GetUrl.generate_twb(logger, server, args)
        else:
            GetUrl.exit_with_error(logger, _("tabcmd.get.extension.not_found"))

    @staticmethod
    def evaluate_file_name(logger, file_name, url):
        type_of_file = None
        if file_name is not None:
            split_file_name = file_name.split(".")
            type_of_file = split_file_name[1]
        else:  # file_name is None:
            # grab from url
            split_url_to_get_extension = url.split(".")
            if len(split_url_to_get_extension) > 1:
                type_of_file = split_url_to_get_extension[1]
            else:
                GetUrl.exit_with_error(logger, _("tabcmd.error.extension.not_found"))
        return type_of_file

    @staticmethod
    def check_if_extension_present(view_name):
        split_view = view_name.split(".")
        if len(split_view) == 2:
            return split_view[1] in ["pdf", "csv", "png", "twb", "twbx"]
        return False

    @staticmethod
    def get_view_without_extension(view_name):
        split_view = view_name.split(".")
        return split_view[0]

    @staticmethod
    def get_workbook(url):
        separated_list = url.split("/")
        if GetUrl.check_if_extension_present(separated_list[::-1][0]):
            view_second_half_url = GetUrl.get_view_without_extension(separated_list[::-1][0])
        else:
            view_second_half_url = separated_list[2]
        return view_second_half_url

    @staticmethod
    def get_view(url):
        # check the size of list
        separated_list = url.split("/")
        if GetUrl.check_if_extension_present(separated_list[::-1][0]):
            view_second_half_url = GetUrl.get_view_without_extension(separated_list[::-1][0])
        else:
            view_second_half_url = separated_list[2]
        return "{}/sheets/{}".format(separated_list[1], view_second_half_url)

    @staticmethod
    def generate_pdf(logger, server, args):
        view = GetUrl.get_view(args.url)
        try:
            views_from_list = GetUrl.get_view_by_content_url(logger, server, view)
            req_option_pdf = TSC.PDFRequestOptions(maxage=1)
            server.views.populate_pdf(views_from_list, req_option_pdf)
            if args.filename is None:
                file_name_with_path = "{}.pdf".format(views_from_list.name)
            else:
                file_name_with_path = args.filename
            formatted_file_name = file_name_with_path
            with open(formatted_file_name, "wb") as f:
                f.write(views_from_list.pdf)
                logger.info(_("export_success"), views_from_list.name, formatted_file_name)
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)

    @staticmethod
    def generate_png(logger, server, args):
        view = GetUrl.get_view(args.url)
        try:
            views_from_list = GetUrl.get_view_by_content_url(logger, server, view)
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            server.views.populate_csv(views_from_list, req_option_csv)
            if args.filename is None:
                file_name_with_path = "{}.png".format(view)
            else:
                file_name_with_path = args.filename
            formatted_file_name = file_name_with_path
            with open(formatted_file_name, "wb") as f:
                f.write(views_from_list.png)
                logger.info(_("export_success"), views_from_list.name, formatted_file_name)
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)

    @staticmethod
    def generate_csv(logger, server, args):
        view = GetUrl.get_view(args.url)
        try:
            views_from_list = GetUrl.get_view_by_content_url(logger, server, view)
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            server.views.populate_csv(views_from_list, req_option_csv)
            if args.filename is None:
                file_name_with_path = "{}.csv".format(view)
            else:
                file_name_with_path = args.filename
            formatted_file_name = file_name_with_path
            with open(formatted_file_name, "wb") as f:
                f.write(views_from_list.csv)
                logger.info(_("export_success"), views_from_list.name, formatted_file_name)
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)

    @staticmethod
    def generate_twb(logger, server, args):
        workbook = GetUrl.get_workbook(args.url)
        try:
            target_workbook = GetUrl.get_view_by_content_url(logger, server, workbook)
            file_target = None
            if args.filename is None:
                file_target = target_workbook.name
            else:
                file_target = args.filename

            server.workbooks.download(target_workbook.id, filepath=file_target, no_extract=False)
            logger.info(_("export_success"), target_workbook.name, file_target)
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)
