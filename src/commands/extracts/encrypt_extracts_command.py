import tableauserverclient as TSC

from src.commands.auth.session import Session
from src.commands.constants import Errors
from src.commands.server import Server
from src.execution.localize import _
from src.execution.logger_config import log


class EncryptExtracts(Server):
    """
    Command that encrypt all extracts on a site.
    If no site is specified, extracts on the default site will be encrypted.
    """

    name: str = "encryptextracts"
    description: str = _("encryptextracts.short_description")

    @staticmethod
    def define_args(encrypt_extract_parser):
        encrypt_extract_parser.add_argument("site_name", metavar="site-name", help=_("editsite.options.site-name"))

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        site_item = Server.get_site_for_command_or_throw(logger, server, args.site_name)
        try:
            logger.info(_("encryptextracts.status").format(site_item.name))
            job = server.sites.encrypt_extracts(site_item.id)
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, e)

        logger.info(_("common.output.job_queued_success"))
        logger.debug("Extract encryption queued with JobID: {}".format(job.id))
