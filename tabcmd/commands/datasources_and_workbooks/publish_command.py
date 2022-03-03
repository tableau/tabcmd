import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.project.project_command import ProjectCommand
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class PublishCommand(DatasourcesAndWorkbooks):
    """
    This command publishes the specified workbook (.twb(x)), data source
    (.tds(x)), or extract (.hyper) to Tableau Server.
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        logger.debug(args)
        session = Session()
        server = session.create_session(args)
        publish_mode = PublishCommand.get_publish_mode(args)
        source = PublishCommand.get_source_type(args)

        if args.project is not None:
            project_id = ProjectCommand.find_project_id(server, args.project)
        else:
            project_id = ""

        if source == "twbx" or source == "twb":
            new_workbook = TSC.WorkbookItem(project_id, name=args.name, show_tabs=args.tabbed)  # TODO
            new_workbook = server.workbooks.publish(new_workbook, args.file_name, publish_mode)
            logger.info("Workbook {} published".format(new_workbook.name))

        elif source == "tds" or source == "tdsx" or source == "hyper":
            new_datasource = TSC.DatasourceItem(project_id, name=args.name)
            new_datasource = server.datasources.publish(new_datasource, args.file_path, publish_mode)
            logger.info("DataSource {} published".format(new_datasource.name))

    @staticmethod
    def get_publish_mode(args):
        if args.overwrite:
            publish_mode = TSC.Server.PublishMode.Overwrite
        else:
            publish_mode = TSC.Server.PublishMode.CreateNew
        return publish_mode

    @staticmethod
    def get_source_type(args):
        source_list = args.source.split(".")
        twbx = "twbx"
        twb = "twb"
        tdsx = "tdsx"
        tds = "tds"
        hyper = "hyper"
        if twbx in source_list:
            return twbx
        elif twb in source_list:
            return twb
        elif tdsx in source_list:
            return tdsx
        elif tds in source_list:
            return tds
        elif hyper in source_list:
            return hyper
