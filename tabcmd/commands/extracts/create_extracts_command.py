from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.extracts.extracts import Extracts
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class CreateExtracts(Server):
    """
    Command that creates extracts for a published workbook or data source.
    """

    name: str = "createextracts"
    description: str = _("createextracts.short_description")

    @staticmethod
    def define_args(create_extract_parser):
        group = create_extract_parser.add_argument_group(title=CreateExtracts.name)
        set_ds_xor_wb_args(group, True)
        set_embedded_datasources_options(group)
        set_encryption_option(group)
        set_project_arg(group)
        set_parent_project_arg(group)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        logger.debug(
            "Extract params: encrypt={}, include_all={}, datasources={}".format(
                args.encrypt, args.include_all, args.embedded_datasources
            )
        )
        try:
            item = Extracts.get_wb_or_ds_for_extracts(args, logger, server)
            if args.datasource:
                logger.info(_("createextracts.for.datasource").format(args.datasource))
                job = server.datasources.create_extract(item, encrypt=args.encrypt)

            else:
                if not args.include_all and not args.embedded_datasources:
                    Errors.exit_with_error(
                        logger,
                        _("extracts.workbook.errors.requires_datasources_or_include_all").format("deleteextracts"),
                    )

                logger.info(_("createextracts.for.workbook_name").format(args.workbook))
                job = server.workbooks.create_extract(
                    item,
                    encrypt=args.encrypt,
                    includeAll=args.include_all,
                    datasources=args.embedded_datasources,
                )
        except Exception as e:

            if args.continue_if_exists and Errors.is_resource_conflict(e):
                logger.info(_("tabcmd.result.already_exists").format(_("content_type.extract"), args.name))
                return
            Errors.exit_with_error(logger, e)

        logger.info(_("common.output.job_queued_success"))
        logger.debug("Extract creation queued with JobID: {}".format(job.id))
