import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class DecryptExtracts(Server):
    """Command that decrypts all extracts on a site. If no site is
    specified, extracts on the default site will be decrypted."""

    name: str = "decryptextracts"
    description: str = _("decryptextracts.short_description")

    @staticmethod
    def define_args(decrypt_extract_parser):
        group = decrypt_extract_parser.add_argument_group(title=DecryptExtracts.name)
        group.add_argument("site_name", metavar="site-name", help=_("editsite.options.site-name"))

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("======================== {} {} =======================".format("tabcmd", __class__.name))
        session = Session()
        server = session.create_session(args, logger)
        site_item = Server.get_site_for_command_or_throw(logger, server, args.site_name)
        try:
            logger.info(_("decryptextracts.status").format(args.site_name))
            job = server.sites.decrypt_extracts(site_item.id)
        except Exception as e:
            Errors.exit_with_error(logger, e)

        logger.info(_("common.output.job_queued_success"))
        logger.debug("Extract decryption queued with JobID: {}".format(job.id))
