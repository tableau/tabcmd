import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class ReencryptExtracts(Server):
    """
    Command to Reencrypt all extracts on a site with new encryption keys.
    This command will regenerate the key encryption key and data encryption key. You must specify a site.
    """

    name: str = "reencryptextracts"
    description: str = _("reencryptextracts.short_description")

    @staticmethod
    def define_args(reencrypt_extract_parser):
        reencrypt_extract_parser.add_argument("site_name", metavar="site-name", help=_("editsite.options.site-name"))

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        site_item = Server.get_site_for_command_or_throw(logger, server, args.site_name)
        try:
            logger.info(_("reencryptextracts.status").format(site_item.name))
            job = server.sites.encrypt_extracts(site_item.id)
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, e)

        logger.info(_("common.output.job_queued_success"))
        logger.debug("Extract re-encryption queued with JobID: {}".format(job.id))
