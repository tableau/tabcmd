from tabcmd.commands.server import Server


class SiteCommand(Server):
    """
    Acts as a base class for site related group of commands
    """

    @staticmethod
    def get_sites(server):
        sites, pagination = server.sites.get()
        return sites

    @staticmethod
    def find_site_id(server, site_name):
        return Server.get_items_by_name(logger, server.sites, site_name)[0].id
