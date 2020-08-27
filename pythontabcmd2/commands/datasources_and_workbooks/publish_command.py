import tableauserverclient as TSC
from .. import log
from ..project.project_command import ProjectCommand
from ... import Session
from .. import PublishParser


class PublishCommand:
    def __init__(self, args, evaluated_project_path, source, filename):
        self.args = args
        self.file_name = filename
        self.file_path = source
        self.project_path = evaluated_project_path
        self.source = self.get_source_type(source)
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.publish',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, evaluated_project_path, source, filename = PublishParser.\
            publish_parser()
        return cls(args, evaluated_project_path, source, filename)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.publish(server_object)

    def publish(self, server):
        if self.args.project is not None:
            project_id = \
                ProjectCommand.find_project_id(server, self.args.project)
        else:
            project_id = ''
        if self.source == "twbx" or self.source == "twb":
            new_workbook = TSC.WorkbookItem(project_id,
                                            name=self.args.name,
                                            show_tabs=self.args.tabbed)  # TODO

            if self.args.overwrite:
                publish_mode = TSC.Server.PublishMode.Overwrite
            else:
                publish_mode = TSC.Server.PublishMode.CreateNew
            new_workbook = server.workbooks.publish(new_workbook,
                                                    self.file_name,
                                                    publish_mode)
            self.logger.info("Workbook {} published".format(
                new_workbook.name))

        elif self.source == "tds" or self.source == "tdsx" or \
                self.source == "hyper":
            new_datasource = TSC.DatasourceItem(project_id,
                                                name=self.args.name)
            if self.args.overwrite:
                publish_mode = TSC.Server.PublishMode.Overwrite
            else:
                publish_mode = TSC.Server.PublishMode.CreateNew
            new_datasource = server.datasources.publish(new_datasource,
                                                        self.file_path,
                                                        publish_mode)
            self.logger.info("DataSource {} published".format(
                new_datasource.name))

    def get_source_type(self, source):
        source_list = source.split('.')
        twbx = 'twbx'
        twb = 'twb'
        tdsx = 'tdsx'
        tds = 'tds'
        hyper = 'hyper'
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
