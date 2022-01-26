class CommandsMap:
    commands_hash_map = {"login": ("LoginCommand", "Sign in to the server"),
                         "get": ("GetUrl", "Get a file from the server"),
                         "createproject": ("CreateProjectCommand",
                                           "Create a project"),
                         "deleteproject": ("DeleteProjectCommand",
                                           "Delete a project"),
                         "creategroup": ("CreateGroupCommand",
                                         "Create a local group"),
                         "deletegroup": ("DeleteGroupCommand",
                                         "Delete a group"),
                         "createusers": ("CreateUserCommand",
                                         "Create users on the server"),
                         "removeusers": ("RemoveUserCommand",
                                         "Remove users from a group"),
                         "export": ("ExportCommand",
                                    "Export the data or image of "
                                    "a view from the server"),
                         "logout": ("LogoutCommand",
                                    "Sign out from the server"),
                         "addusers": ("AddUserCommand",
                                      "Add users to a group"),
                         "createsiteusers": ("CreateSiteUsersCommand",
                                             "Create users on the "
                                             "current site"),
                         "createsite": ("CreateSiteCommand", "Create a site"),
                         "deletesite": ("DeleteSiteCommand", "Delete a site"),
                         "deletesiteusers": ("DeleteSiteUsersCommand",
                                             "Delete site users"),
                         "editsite": ("EditSiteCommand", "Edit a site"),
                         "listsites": ("ListSiteCommand",
                                       "List sites for user"),
                         "delete": ("DeleteCommand", "Delete a workbook or "
                                                     "data source "
                                                     "from the server"),
                         "publish": ("PublishCommand",
                                     "Publish a workbook, data source, "
                                     "or extract to the server"),
                         "createextracts": (
                             "CreateExtracts",
                             "Create extracts for a published workbook "
                             "or data source"),
                         "decryptextracts": ("DecryptExtracts",
                                             "Decrypt extracts on a site"),
                         "deleteextracts": ("DeleteExtracts",
                                            "Delete extracts for a published "
                                            "workbook or data source"),
                         "encryptextracts": ("EncryptExtracts",
                                             "Encrypt extracts on a site"),
                         "reencryptextracts": ("ReencryptExtracts",
                                               "Reencrypt extracts on a site"),
                         "refreshextracts": ("RefreshExtracts",
                                             "Refresh the extracts of a "
                                             "workbook or data "
                                             "source on the server"),
                         "publishsamples": ("PublishSamplesCommand",
                                            "publish samples to the server"),
                         "help": ("HelpCommand", "Help for tabcmd2 commands")}
