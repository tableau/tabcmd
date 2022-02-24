import sys


class Commands:
    def __init__(self, args):
        self.logger = None
        self.username = args.username
        self.password = args.password
        self.server = args.server
        self.site = args.site
        self.token_name = args.token_name
        self.personal_token = args.token
        self.logging_level = args.logging_level

    @staticmethod
    def get_workbook_item(server, workbook_name):
        workbook_item = None
        all_workbooks_items, pagination_item = server.workbooks.get()
        for workbook in all_workbooks_items:
            if workbook.name == workbook_name:
                workbook_item = workbook
                break
        return workbook_item

    @staticmethod
    def get_data_source_item(server, data_source_name):
        data_source_item = None
        all_datasources, pagination_item = server.datasources.get()
        for datasource in all_datasources:
            if datasource.name == data_source_name:
                data_source_item = datasource
                break
        return data_source_item

    @staticmethod
    def get_workbook_id(server, workbook_name):
        all_workbooks_items, pagination_item = server.workbooks.get()
        workbook_id = None
        for workbook in all_workbooks_items:
            if workbook.name == workbook_name:
                workbook_id = workbook.id
                break
        return workbook_id

    @staticmethod
    def get_data_source_id(server, datasource_name):
        all_datasources, pagination_item = server.datasources.get()
        datasource_id = None
        for datasource in all_datasources:
            if datasource.name == datasource_name:
                datasource_id = datasource.id
                break
        return datasource_id

    @staticmethod
    def exit_with_error(logger, message, exception=None):
        if exception:
            logger.error(message, exception)
        else:
            logger.error(message)
        sys.exit(1)
