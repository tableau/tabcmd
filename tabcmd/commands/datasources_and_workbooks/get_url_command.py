import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class GetUrl(DatasourcesAndWorkbooks):
    """
    This command gets the resource from Tableau Server that's represented
    by the specified (partial) URL. The result is returned as a file.
    """

    name: str = "get"
    description: str = _("get.short_description")

    @staticmethod
    def define_args(get_url_parser):
        get_url_parser.add_argument("url", help=_("refreshextracts.options.url"))
        set_filename_arg(get_url_parser)
        # these don't need arguments, although that would be a good future addition
        # tabcmd get "/views/Finance/InvestmentGrowth.png?:size=640,480" -f growth.png
        # tabcmd get "/views/Finance/InvestmentGrowth.png?:refresh=yes" -f growth.png

    @staticmethod
    def run_command(args):
        # A view can be returned in PDF, PNG, or CSV (summary data only) format.
        # A Tableau workbook is returned as a TWB if it connects to a datasource/live connection,
        # or a TWBX if it uses an extract.
        # A Tableau datasource is returned as a TDS if it connects to a live connection,
        # or a TDSX if it uses an extract.
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        if " " in args.url:
            Errors.exit_with_error(logger, _("export.errors.white_space_workbook_view"))

        file_type = GetUrl.get_file_type_from_filename(logger, args.filename, args.url)
        content_type = GetUrl.evaluate_content_type(logger, args.url)
        if content_type == "workbook":
            if file_type == "twbx" or file_type == "twb":
                GetUrl.generate_twb(logger, server, args, file_type)
            else:
                Errors.exit_with_error(
                    logger, message=_("publish.errors.mutually_exclusive_option").format("twb", "twbx") #TODO
                )
        if content_type == "datasource":
            if file_type == "tdsx" or file_type == "tds":
                GetUrl.generate_tds(logger, server, args, file_type)
            else:
                Errors.exit_with_error(
                    logger, message=_("publish.errors.mutually_exclusive_option").format("tds", "tdsx") #TODO
                )
        else:  # content type = view
            if file_type == "pdf":
                GetUrl.generate_pdf(logger, server, args)
            elif file_type == "png":
                GetUrl.generate_png(logger, server, args)
            elif file_type == "csv":
                GetUrl.generate_csv(logger, server, args)
            else:
                Errors.exit_with_error(logger, message=_("tabcmd.get.extension.not_found")) #TODO

    @staticmethod
    def evaluate_content_type(logger, url):
        # specify a view to get using "/views/<workbookname>/<viewname>.<extension>"
        # specify a workbook to get using "/workbooks/<workbookname>.<extension>".
        # specify a datasource to get using "/datasources/<datasourcename>.<extension>"
        if url.find("/views/") == 0:
            return "view"
        elif url.find("/workbooks/") == 0:
            return "workbook"
        elif url.find("/datasources/") == 0:
            return "datasource"
        else:
            Errors.exit_with_error(
                logger, message=_("export.errors.requires_workbook_view_param").format(__class__.__name__)
            )

    @staticmethod
    def get_file_type_from_filename(logger, file_name, url):
        type_of_file = None
        file_name = file_name or url
        logger.debug(_("get.options.file") + ": {}".format(file_name))
        type_of_file = GetUrl.get_file_extension(file_name)

        if not type_of_file:
            Errors.exit_with_error(logger, _("tabcmd.get.extension.not_found").format(file_name)) #TODO
        else:
            logger.debug("filetype: {}".format(type_of_file))
            if type_of_file in ["pdf", "csv", "png", "twb", "twbx", "tdsx"]:
                return type_of_file

        Errors.exit_with_error(logger, _("tabcmd.get.extension.not_found").format(file_name)) #TODO

    @staticmethod
    def get_file_extension(filename):
        parts = filename.split(".")
        if len(parts) < 2:
            return None
        extension = parts[1]
        extension = GetUrl.strip_query_params(extension)
        return extension

    @staticmethod
    def strip_query_params(filename):
        if filename.find("?") > 0:
            filename = filename.split("?")[0]
        return filename

    @staticmethod
    def get_name_without_possible_extension(filename):
        if filename.find(".") > 0:
            filename = filename.split(".")[0]
        return filename

    @staticmethod
    def get_resource_name(logger, url):  # /<resource-name>/r-name" -> "r-name"
        name_parts = url.split("/")
        if len(name_parts) != 3:
            raise ValueError(_("export.errors.requires_workbook_view_param").format(GetUrl.name)) #TODO
        resource_name = name_parts[::-1][0]  # last part
        resource_name = GetUrl.strip_query_params(resource_name)
        resource_name = GetUrl.get_name_without_possible_extension(resource_name)
        return resource_name

    @staticmethod
    def get_view_url(url):  # "/views/wb-name/view-name" -> wb-name/sheets/view-name
        name_parts = url.split("/")  # ['', 'views', 'wb-name', 'view-name']
        if len(name_parts) != 4:
            raise ValueError(_("export.errors.requires_workbook_view_param").format(GetUrl.name))
        view_name = name_parts[::-1][0]
        view_name = GetUrl.strip_query_params(view_name)
        view_name = GetUrl.get_name_without_possible_extension(view_name)
        workbook_name = name_parts[2]
        return DatasourcesAndWorkbooks.get_view_url_from_names(workbook_name, view_name)

    @staticmethod
    def filename_from_args(file_argument, item_name, filetype):
        if file_argument is None:
            file_argument = "{}.{}".format(item_name, filetype)
        return file_argument

    @staticmethod
    def generate_pdf(logger, server, args):
        view_url = GetUrl.get_view_url(args.url)
        try:
            view_item: TSC.ViewItem = GetUrl.get_view_by_content_url(logger, server, view_url)
            logger.debug(_("content_type.view") + ": {}".format(view_item.name))
            req_option_pdf = TSC.PDFRequestOptions(maxage=1)
            server.views.populate_pdf(view_item, req_option_pdf)
            filename = GetUrl.filename_from_args(args.filename, view_item.name, "pdf")
            with open(filename, "wb") as f:
                f.write(view_item.pdf)
            logger.info(_("export.success").format(view_item.name, filename))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)

    @staticmethod
    def generate_png(logger, server, args):
        view = GetUrl.get_view_url(args.url)
        try:
            view_item: TSC.ViewItem = GetUrl.get_view_by_content_url(logger, server, view)
            logger.debug(_("content_type.view") + ": {}".format(view_item.name))
            req_option_csv = TSC.CSVRequestOptions(maxage=1)  # same as png
            server.views.populate_image(view_item, req_option_csv)
            filename = GetUrl.filename_from_args(args.filename, view_item.name, "png")
            with open(filename, "wb") as f:
                f.write(view_item.image)
            logger.info(_("export.success").format(view_item.name, filename))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)

    @staticmethod
    def generate_csv(logger, server, args):
        view_url = GetUrl.get_view_url(args.url)
        try:
            view_item: TSC.ViewItem = GetUrl.get_view_by_content_url(logger, server, view_url)
            logger.debug(_("content_type.view") + ": {}".format(view_item.name))
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            server.views.populate_csv(view_item, req_option_csv)
            file_name_with_path = GetUrl.filename_from_args(args.filename, view_item.name, "csv")
            with open(file_name_with_path, "wb") as f:
                f.writelines(view_item.csv)
            logger.info(_("export.success").format(view_item.name, file_name_with_path))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def generate_twb(logger, server, args, file_extension):
        workbook_name = GetUrl.get_resource_name(logger, args.url)

        try:
            target_workbook = GetUrl.get_wb_by_content_url(logger, server, workbook_name)
            logger.debug(_("content_type.workbook") + ": {}".format(workbook_name))
            file_name_with_path = GetUrl.filename_from_args(args.filename, workbook_name, file_extension)
            logger.debug("Saving as {}".format(file_name_with_path))
            server.workbooks.download(target_workbook.id, filepath=None, no_extract=False)
            logger.info(_("export.success").format(target_workbook.name, file_name_with_path))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)
            
    @staticmethod
    def generate_tds(logger, server, args, file_extension):
        datasource_name = GetUrl.get_resource_name(logger, args.url)
    
        try:
            target_datasource = GetUrl.get_ds_by_content_url(logger, server, datasource_name)
            logger.debug(_("content_type.datasource") + ": {}".format(datasource_name))
            file_name_with_path = GetUrl.filename_from_args(args.filename, datasource_name, file_extension)
            logger.debug("Saving as {}".format(file_name_with_path))
            server.datasources.download(target_datasource.id, filepath=None, no_extract=False)
            logger.info(_("export.success").format(target_datasource.name, file_name_with_path))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)
