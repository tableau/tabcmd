from enum import IntEnum
from typing import List, Callable, Dict, NoReturn
from tabcmd.commands.server import Server
from tabcmd.commands.constants import Errors

import io
import tableauserverclient as TSC


class Userdata:
    def __init__(self):
        self.name = None
        self.password = None
        self.fullname = None
        self.license_level = None
        self.admin_level = None
        self.publisher = None
        self.email = None
        self.auth = None

    def populate(self, values: List[str]) -> NoReturn:
        self.__init__()  # populate all with None
        n_values = len(values)
        self.name = values[0]
        if n_values >= 2:
            self.password = values[1]
        if n_values >= 3:
            self.fullname = values[2]
        if n_values >= 4:
            self.license_level = values[3]
        if n_values >= 5:
            self.admin_level = values[4]
        if n_values >= 6:
            self.publisher = values[5]
        if n_values >= 7:
            self.email = values[6]
        if n_values >= 8:
            self.auth = values[7]

    def to_tsc_user(self):
        site_role = UserCommand.evaluate_site_role(self.license_level, self.admin_level, self.publisher)
        if not site_role:
            raise AttributeError("Site role is required")
        user = TSC.UserItem(self.name, site_role, self.auth)
        user.email = self.email
        user.fullname = self.fullname
        return user


CHOICES = [
    [],
    [],
    [],
    ["creator", "explorer", "viewer", "unlicensed"],  # license
    ["system", "site", "none", "no"],  # admin
    ["yes", "true", "1", "no", "false", "0"],  # publisher
    [],
    [TSC.UserItem.Auth.SAML, TSC.UserItem.Auth.OpenID, TSC.UserItem.Auth.ServerDefault],  # auth
]


# username, password, display_name, license, admin_level, publishing, email
class Column(IntEnum):
    USERNAME = 0
    PASS = 1
    DISPLAY_NAME = 2
    LICENSE = 3  # aka site role
    ADMIN = 4
    PUBLISHER = 5
    EMAIL = 6
    AUTH = 7

    MAX = 7


class UserCommand(Server):
    """
    This class acts as a base class for user related group of commands
    """

    # used in createusers, createsiteusers
    @staticmethod
    def validate_file_for_import(csv_file: io.TextIOWrapper, logger, detailed=False, strict=False) -> int:
        num_errors = 0
        num_lines = 0
        csv_file.seek(0)  # set to start of file in case it has been read earlier
        line = csv_file.readline()  # this is a string when running 
        while line and line != "":
            try:
                if detailed:
                    # do not print passwords
                    UserCommand._validate_user_or_throw(line, logger)
                else:
                    logger.debug("username - {}".format(line))
                    UserCommand._validate_username_or_throw(line)
                num_lines += 1
            except Exception as exc:
                logger.info("invalid line [{0}]: {1}".format(line, exc))
                num_errors += 1
            line = csv_file.readline()
        if strict and num_errors > 0:
            Errors.exit_with_error(
                logger, "Invalid users in file - please fix {} problems and try again.".format(num_errors)
            )
        return num_lines

    # valid: username, domain/username, username@domain, domain/username@email
    @staticmethod
    def _validate_username_or_throw(username) -> NoReturn:
        if username is None or username == "" or username.strip(" ") == "":
            raise AttributeError("Username must be specified in csv file")
        if username.find(" ") >= 0:
            raise AttributeError("Username cannot contain spaces")
        at_symbol = username.find("@")

        if at_symbol >= 0:
            username = username[:at_symbol] + "X" + username[at_symbol + 1 :]
            if username.find("@") >= 0:
                raise AttributeError(
                    "If a user name includes an @ character that represents anything other than a domain separator, "
                    "you need to refer to the symbol using the hexadecimal format: \\0x40"
                )

    @staticmethod
    def _validate_user_or_throw(incoming, logger) -> NoReturn:
        line = list(map(str.strip, incoming.split(",")))
        logger.debug("details - {}".format(line[0]))
        if len(line) > Column.MAX:
            raise AttributeError(
                "The file contains {} columns, but there are only {} valid columns in a user \
                 import csv file".format(
                    len(line), Column.MAX
                )
            )
        username = line[Column.USERNAME.value]
        UserCommand._validate_username_or_throw(username)
        for column_type in range(1, len(line) - 1):
            logger.debug("column {}".format(column_type), line[column_type])
            UserCommand._validate_item(line[column_type], column_type)

    @staticmethod
    def _validate_item(item: str, column_type: int) -> NoReturn:
        if item is None or item == "":
            # value can be empty for any column except user, which is checked elsewhere
            return
        if item in CHOICES[column_type] or CHOICES[column_type] == []:
            return
        raise AttributeError("Invalid value for {0}: {1}".format(Column[column_type].name, item))

    @staticmethod
    def get_users_from_file(csv_file: io.TextIOWrapper, logger=None) -> List[TSC.UserItem]:
        csv_file.seek(0)  # set to start of file in case it has been read earlier
        if logger:
            logger.debug("Reading from file {}".format(csv_file.name))
        user_list = []
        line = csv_file.readline()
        if logger:
            logger.debug("> {}".format(line))
        while line and not line == "":
            user: TSC.UserItem = UserCommand._parse_line(line)
            user_list.append(user)
            line = csv_file.readline()
        return user_list

    @staticmethod
    def _parse_line(line: str) -> TSC.UserItem:
        if line is None:
            return None
        if line is False or line == "\n" or line == "":
            return None
        line: str = line.strip().lower()
        line_parts: List[str] = line.split(",")
        data = Userdata()
        values: List[str] = list(map(str.strip, line_parts))
        data.populate(values)
        return data.to_tsc_user()

    # https://help.tableau.com/current/server/en-us/csvguidelines.htm#settings_and_site_roles
    @staticmethod
    def evaluate_site_role(license_level, admin_level, publisher):
        if not license_level or not admin_level or not publisher:
            return "Unlicensed"
        # ignore case everywhere
        license_level = license_level.lower()
        admin_level = admin_level.lower()
        publisher = publisher.lower()
        site_role = None
        # don't need to check publisher for system/site admin
        if admin_level == "system":
            site_role = "SiteAdministrator"
        elif admin_level == "site":
            if license_level == "creator":
                site_role = "SiteAdministratorCreator"
            elif license_level == "explorer":
                site_role = "SiteAdministratorExplorer"
            else:
                site_role = "SiteAdministratorExplorer"
        else:  # if it wasn't 'system' or 'site' then we can treat it as 'none'
            if publisher == "yes":
                if license_level == "creator":
                    site_role = "Creator"
                elif license_level == "explorer":
                    site_role = "ExplorerCanPublish"
                else:
                    site_role = "Unlicensed"  # is this the expected outcome?
            else:  # publisher == 'no':
                if license_level == "explorer" or license_level == "creator":
                    site_role = "Explorer"
                elif license_level == "viewer":
                    site_role = "Viewer"
                else:  # if license_level == 'unlicensed'
                    site_role = "Unlicensed"
        if site_role is None:
            site_role = "Unlicensed"
        return site_role

    @staticmethod
    def act_on_users(logger: object, server: object, action_name: str, server_method: Callable, args: Dict) -> NoReturn:
        n_users_handled: int = 0
        number_of_errors: int = 0
        n_users_listed: int = UserCommand.validate_file_for_import(args.users, logger, strict=args.require_all_valid)
        logger.debug("Found {} users in file".format(n_users_listed))

        try:
            group = UserCommand.find_group(logger, server, args.name)
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Could not get group", exception=e)
        user_obj_list: List[TSC.UserItem] = UserCommand.get_users_from_file(args.users)
        logger.debug("Successfully parsed {} users".format(len(user_obj_list)))
        for user_obj in user_obj_list:
            username: str = user_obj.name
            try:
                user_id: str = UserCommand.find_user_id(logger, server, username)
                logger.debug("{} user {} ({})".format(action_name, username, user_id))
            except TSC.ServerResponseError as e:
                Errors.check_common_error_codes_and_explain(logger, e)
                number_of_errors += 1
                user_id = None
                logger.debug("Skipping user {}".format(username))
                continue

            try:
                server_method(group, user_id)
                n_users_handled += 1
                logger.info("Successfully {0} {1} for group {2}".format(action_name, username, group))
            except TSC.ServerResponseError as e:
                Errors.check_common_error_codes_and_explain(logger.info, e)
                number_of_errors += 1
                logger.debug("Error at user {}".format(username))
        logger.info("======== 100% complete ========")
        logger.info("======== Number of users listed: {} =========".format(n_users_listed))
        logger.info("======== Number of users {}: {} =========".format(action_name, n_users_handled))
        if number_of_errors > 0:
            logger.info("======== Number of errors {} =========".format(number_of_errors))
