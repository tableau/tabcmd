from tabcmd.parsers.add_users_parser import *
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
    parsers_hashmap = {"login": LoginParser.login_parser,
                       "get": GetUrlParser.get_url_parser,
                       "createproject":
                           CreateProjectParser.create_project_parser,
                       "deleteproject":
                           DeleteProjectParser.delete_project_parser,
                       "creategroup":
                           CreateGroupParser.create_group_parser,
                       "deletegroup":
                           DeleteGroupParser.delete_group_parser,
                       "createusers":
                           CreateUserParser.create_user_parser,
                       "removeusers":
                           RemoveUserParser.remove_user_parser,
                       "export": ExportParser.export_parser,
                       "logout": LogoutParser.logout_parser,
                       "addusers": AddUserParser.add_user_parser,
                       "createsiteusers":
                           CreateSiteUsersParser.create_site_user_parser,
                       "createsite": CreateSiteParser.create_site_parser,
                       "deletesite": DeleteSiteParser.delete_site_parser,
                       "deletesiteusers":
                           DeleteSiteUsersParser.delete_site_users_parser,
                       "editsite": EditSiteParser.edit_site_parser,
                       "listsites": ListSitesParser.list_site_parser,
                       "delete": DeleteParser.delete_parser,
                       "publish": PublishParser.publish_parser,
                       "createextracts":
                           CreateExtractsParser.create_extracts_parser,
                       "decryptextracts":
                           DecryptExtractsParser.decrypt_extracts_parser,
                       "deleteextracts":
                           DeleteExtractsParser.delete_extracts_parser,
                       "encryptextracts":
                           EncryptExtractsParser.encrypt_extracts_parser,
                       "reencryptextracts":
                           ReencryptExtractsParser.reencrypt_extracts_parser,
                       "refreshextracts":
                           RefreshExtractsParser.refresh_extracts_parser,
                       "publishsamples":
                           PublishSamplesParser.publish_samples_parser,
                       "help": HelpParser.help_parser}
