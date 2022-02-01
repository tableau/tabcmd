import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import CreateExtractsParser
from ..project.project_command import ProjectCommand
from ..extracts.extracts_command import ExtractsCommand


class CreateExtracts(ExtractsCommand):
    """
    Command that creates extracts for a published workbook or data source.
    """

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.createextracts_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args = CreateExtractsParser.create_extracts_parser()
        return cls(args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.create_extract(server_object)

    def create_extract(self, server):
        if self.args.datasource:
            try:
                data_source_item = ExtractsCommand. \
                    get_data_source_item(server, self.args.datasource)

                job = server.datasources.create_extract(data_source_item,
                                                        encrypt=self.args.
                                                        encrypt)
                self.logger.info("Extract started Successfully with "
                                 "JobID: {}".format(job.id))
            except TSC.ServerResponseError as e:
                self.logger.error('Server Error', e)
        elif self.args.workbook:
            try:
                project_id = ProjectCommand.find_project_id(server,
                                                            self.args.project)
                workbook_item = ExtractsCommand.get_workbook_item(server,
                                                                  self.args
                                                                  .workbook)
                job = server.workbooks.create_extract(workbook_item,
                                                      encrypt=self.args.
                                                      encrypt,
                                                      includeAll=self.args.
                                                      include_all,
                                                      datasources=self.args.
                                                      embedded_datasources)

                self.logger.info("Extract started successfully with "
                                 "JobID: {}".format(job.id))
            except TSC.ServerResponseError as e:
                self.logger.error('Server Error', e)
