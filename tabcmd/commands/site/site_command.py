from tabcmd.commands.commands import Commands


class SiteCommand(Commands):
    """
    Acts as a base class for site related group of commands
    """

    @staticmethod
    def get_sites(server):
        sites, pagination = server.sites.get()
        return sites

    @staticmethod
    def find_site_id(server, site_name):
        return Commands.get_items_by_name(logger, server.sites, site_name)[0].id
