from tabcmd.parsers.command_parsers import *
from tabcmd.parsers.create_extracts_parser import *
from tabcmd.parsers.create_group_parser import *
from tabcmd.parsers.create_project_parser import *
from tabcmd.parsers.create_site_parser import *
from tabcmd.parsers.create_site_users_parser import *
from tabcmd.parsers.create_users_parser import *
from tabcmd.parsers.decrypt_extracts_parser import *
from tabcmd.parsers.delete_extracts_parser import *
from tabcmd.parsers.delete_group_parser import *
from tabcmd.parsers.delete_parser import *
from tabcmd.parsers.delete_project_parser import *
from tabcmd.parsers.delete_site_parser import *
from tabcmd.parsers.delete_site_users_parser import *
from tabcmd.parsers.edit_site_parser import *
from tabcmd.parsers.encrypt_extracts_parser import *
from tabcmd.parsers.export_parser import *
from tabcmd.parsers.get_url_parser import *
from tabcmd.parsers.help_parser import *
from tabcmd.parsers.list_sites_parser import *
from tabcmd.parsers.login_parser import *
from tabcmd.parsers.logout_parser import *
from tabcmd.parsers.publish_parser import *
from tabcmd.parsers.publish_samples_parser import *
from tabcmd.parsers.reencrypt_parser import *
from tabcmd.parsers.refresh_extracts_parser import *
from tabcmd.parsers.remove_users_parser import *


class ParsersMap:
    parsers_hashmap = {
        "addusers": AddUserParser.define_args,
        "createextracts": CreateExtractsParser.define_args,
        "creategroup": CreateGroupParser.define_args,
        "createproject": CreateProjectParser.define_args,
        "createsite": CreateSiteParser.define_args,
        "createsiteusers": CreateSiteUsersParser.define_args,
        "createusers": CreateUserParser.define_args,
        "decryptextracts": DecryptExtractsParser.define_args,
        "delete": DeleteParser.define_args,
        "deleteextracts": DeleteExtractsParser.define_args,
        "deletegroup": DeleteGroupParser.define_args,
        "deleteproject": DeleteProjectParser.define_args,
        "deletesite": DeleteSiteParser.define_args,
        "deletesiteusers": DeleteSiteUsersParser.define_args,
        "editsite": EditSiteParser.define_args,
        "encryptextracts": EncryptExtractsParser.define_args,
        "export": ExportParser.define_args,
        "get": GetUrlParser.define_args,
        "help": HelpParser.define_args,
        "listsites": ListSitesParser.define_args,
        "login": LoginParser.define_args,
        "logout": LogoutParser.define_args,
        "publish": PublishParser.define_args,
        "publishsamples": PublishSamplesParser.define_args,
        "reencryptextracts": ReencryptExtractsParser.define_args,
        "refreshextracts": RefreshExtractsParser.define_args,
        "removeusers": RemoveUserParser.define_args,
    }
