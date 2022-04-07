from enum import IntEnum
from typing import List, Callable, Dict, NoReturn
from tabcmd.commands.server import Server
from tabcmd.commands.constants import Errors

import io
import tableauserverclient as TSC


class Userdata:
    def __init__(self):
        self.username = None
        self.password = None
        self.full_name = None
        self.license_level = None
        self.admin_level = None
        self.publisher = None
        self.email = None
        self.site_role = None


license_roles = ["creator", "explorer", "viewer", "unlicensed"]
admin_roles = ["system", "site", "none"]
publish_options = ["yes", "true", "1", "no", "false", "0"]


# username, password, display_name, license, admin_level, publishing, email
class Column(IntEnum):
    USERNAME = 0
    PASS = 1
    DISPLAY_NAME = 2
    LICENSE = 3
    ADMIN = 4
    PUBLISHER = 5
    EMAIL = 6


class UserCommand(Server):
    """
    This class acts as a base class for user related group of commands
    """

    # used in createusers, createsiteusers
    @staticmethod
    def validate_file_for_import(csv_file: io.TextIOWrapper, logger, detailed=False, strict=False):
        num_errors = 0
        num_lines = 0
        csv_file.seek(0)  # set to start of file in case it has been read earlier
        line = csv_file.readline()
        while line and line != "":
            try:
                if detailed:
                    logger.debug("details - {}".format(line))
                    UserCommand.validate_user_detail_line(line)
                else:
                    logger.debug("username - {}".format(line))
                    UserCommand.validate_username(line)
                num_lines += 1

            except Exception as exc:
                logger.info("invalid line [{0}]: {1}".format(line, exc))
                num_errors += 1
            line = csv_file.readline()
        if strict and num_errors > 0:
            UserCommand.exit_with_error(
                logger, "Invalid users in file - please fix {} problems and try again.".format(num_errors)
            )

        return num_lines

    # valid: username, domain/username, username@domain, domain/username@email
    @staticmethod
    def validate_username(username):
        if username is None or username == "" or username.strip(" ") == "":
            raise AttributeError("Username must be specified in csv file")
        if username.find(" ") >= 0:
            raise AttributeError("Username cannot contain spaces")
        at_symbol = username.find("@")

        if at_symbol >= 0:
            username = username[:at_symbol] + "X" + username[at_symbol + 1:]
            if username.find("@") >= 0:
                raise AttributeError(
                    "If a user name includes an @ character that represents anything other than a domain separator, "
                    "you need to refer to the symbol using the hexadecimal format: \\0x40"
                )

    @staticmethod
    def validate_user_detail_line(incoming):
        line = list(map(str.strip, incoming.split(",")))
        if len(line) > 7:
            raise AttributeError(
                "The file contains {} columns, but there are only 7 valid columns in a user \
             import csv file".format(
                    len(line)
                )
            )
        username = line[Column.USERNAME.value]
        UserCommand.validate_username(username)
        for i in range(1, len(line) - 1):
            if not UserCommand.validate_item(line[i], Column(i)):
                raise AttributeError("Invalid value for {0}: {1}".format(Column[i].name, line[i]))

    @staticmethod
    def validate_item(item, type):
        if item is None or item == "":
            # value can be empty for any column except user, which is checked elsewhere
            return True
        if (
                type == Column.LICENSE.value and item in license_roles
                or type == Column.ADMIN.value and item in admin_roles
                or type == Column.PUBLISHER.value and item in publish_options
        ):
            return True
        return True

    @staticmethod
    def get_users_from_file(csv_file: io.TextIOWrapper, logger=None) -> List[Userdata]:
        csv_file.seek(0)  # set to start of file in case it has been read earlier
        if logger:
            logger.debug("Reading from file {}".format(csv_file.name))
        user_list = []
        line = csv_file.readline()
        if logger:
            logger.debug("> {}".format(line))
        while line:
            users_data = UserCommand.parse_line(line)
            user_list.append(users_data)
            line = csv_file.readline()
        return user_list

    @staticmethod
    def parse_line(line) -> Userdata:
        if line is None:
            return None
        if line is False or line == "\n" or line == "":
            return None
        line = line.strip().lower()
        split_line = list(map(str.strip, line.split(",")))
        if len(split_line) == 1:
            return UserCommand.get_simple_user(split_line[0])
        else:
            return UserCommand.get_user_details(split_line)

    @staticmethod
    def get_simple_user(value):
        user_data = Userdata()
        user_data.username = value
        return user_data

    @staticmethod
    def get_user_details(values):
        user_data = Userdata()
        user_data.username = values[0]
        user_data.password = values[1]
        user_data.full_name = values[2]
        user_data.license_level = values[3]
        user_data.admin_level = values[4]
        user_data.publisher = values[5]
        user_data.email = values[6]
        user_data.site_role = UserCommand.evaluate_license_level_admin_level(
            user_data.license_level, user_data.admin_level, user_data.publisher
        )
        return user_data

    # https://help.tableau.com/current/server/en-us/csvguidelines.htm#settings_and_site_roles
    @staticmethod
    def evaluate_license_level_admin_level(license_level, admin_level, publisher):
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

