import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import PublishParser


class PublishCommand:
    def __init__(self, args, evaluated_project_path, source, filename):
        self.args = args
        self.file_name = filename
        self.project_path = evaluated_project_path
        self.source = source
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.publish',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, evaluated_project_path, source, filename = PublishParser.publish_parser()
        return cls(args, evaluated_project_path, source, filename)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.publish(server_object)

    def publish(self, server):

        new_workbook = TSC.WorkbookItem('', name=self.args.name,
                                        show_tabs=self.args.tabbed)  # TODO
        # PROJECTNAME ->
        # USER ->
        # FETCH ID
        if self.args.overwrite:
            publish_mode = TSC.Server.PublishMode.Overwrite
        else:
            publish_mode = TSC.Server.PublishMode.CreateNew
        new_workbook = server.workbooks.publish(new_workbook,
                                                self.file_name,
                                                publish_mode)
        print("Workbook published. JOB ID: {0}".format(new_workbook.id))
