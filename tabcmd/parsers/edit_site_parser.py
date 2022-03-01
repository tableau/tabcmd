class EditSiteParser:
    """
    Parser for the command editsite
    """

    @staticmethod
    def edit_site_parser(manager, command):
        """Method to parse edit site arguments passed by the user"""
        edit_site_parser = manager.include(command)
        edit_site_parser.add_argument("sitename", help="name of site to update")
        edit_site_parser.add_argument("--site-name", default=None, dest="target", help="new name of site")
        edit_site_parser.add_argument("--site-id", default=None, help="id of site")
        edit_site_parser.add_argument("--url", default=None, help="url of site")
        edit_site_parser.add_argument(
            "--user-quota",
            type=int,
            default=None,
            help="Max number of user that can be added to site",
        )
        edit_site_parser.add_argument(
            "--status",
            default=None,
            help="Set to ACTIVE to activate a site, or to SUSPENDED to suspend a site.",
        )
        edit_site_parser.add_argument(
            "--extract-encryption-mode",
            default=None,
            help="The extract encryption mode for the site can be enforced, enabled or disabled",
        )
        edit_site_parser.add_argument(
            "--run-now-enabled",
            default=None,
            help="Allow or deny users from running extract refreshes, flows, or schedules manually.",
        )
        edit_site_parser.add_argument(
            "--storage-quota",
            type=int,
            default=None,
            help="in MB amount of workbooks, extracts data sources stored on site",
        )
        group = edit_site_parser.add_mutually_exclusive_group()
        group.add_argument(
            "--site-mode",
            default=None,
            help="Does not allow site admins to add or remove users",
        )
        group.add_argument(
            "--no-site-mode",
            default=None,
            help="Allows site admins to add or remove users",
        )
