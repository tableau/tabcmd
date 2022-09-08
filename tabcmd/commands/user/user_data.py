import argparse
import io
import logging
from enum import IntEnum
from typing import List, Callable, Optional

import tableauserverclient as TSC

from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _


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

    def populate(self, values: List[str]) -> None:
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

    def to_tsc_user(self) -> TSC.UserItem:
        site_role = UserCommand.evaluate_site_role(self.license_level, self.admin_level, self.publisher)
        if not site_role:
            raise AttributeError("Site role is required")
        user = TSC.UserItem(self.name, site_role, self.auth)
        user.email = self.email
        user.fullname = self.fullname
        return user


CHOICES: List[List[str]] = [
    [],
    [],
    [],
    ["creator", "explorer", "viewer", "unlicensed"],  # license
    ["system", "site", "none", "no"],  # admin
    ["yes", "true", "1", "no", "false", "0"],  # publisher
    [],
    [TSC.UserItem.Auth.SAML, TSC.UserItem.Auth.OpenID, TSC.UserItem.Auth.ServerDefault],  # auth
]


# username, password, display_name, license, admin_level, publishing, email, auth type
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

    # read the file containing usernames or user details and validate each line
    # log out any errors encountered
    # returns the number of valid lines in the file
    # @param boolean strict: if true, die if any errors are found
    @staticmethod
    def validate_file_for_import(csv_file: io.TextIOWrapper, logger, detailed=False, strict=False) -> int:
        num_errors = 0
        num_valid_lines = 0
        csv_file.seek(0)  # set to start of file in case it has been read earlier
        line: str = csv_file.readline()
        while line and line != "":
            try:
                printable_line = line
                if detailed:
                    # do not print passwords
                    printable_line = line.split(",")[0]
                    UserCommand._validate_user_or_throw(line, logger)
                else:
                    logger.debug("> username - {}".format(line))
                    UserCommand._validate_username_or_throw(line)
                num_valid_lines += 1
            except Exception as exc:
                logger.info(_("importcsvsummary.error.line").format(printable_line, exc, ""))
                num_errors += 1
            line = csv_file.readline()
        if strict and num_errors > 0:
            Errors.exit_with_error(logger, _("importcsvsummary.error.too_many_errors"))
        return num_valid_lines

    # valid: username, domain/username, username@domain, domain/username@email
    @staticmethod
    def _validate_username_or_throw(username) -> None:
        if username is None or username == "" or username.strip(" ") == "":
            raise AttributeError(_("user.input.name.err.empty"))
        if username.find(" ") >= 0:
            raise AttributeError(_("tabcmd.report.error.user.no_spaces_in_username"))
        at_symbol = username.find("@")

        if at_symbol >= 0:
            username = username[:at_symbol] + "X" + username[at_symbol + 1 :]
            if username.find("@") >= 0:
                raise AttributeError(_("tabcmd.report.error.user_csv.at_char"))

    @staticmethod
    def _validate_user_or_throw(incoming, logger) -> None:
        line = list(map(str.strip, incoming.split(",")))
        logger.debug("> details - {}".format(line[0]))
        if len(line) > Column.MAX:
            raise AttributeError(_("tabcmd.report.error.user_csv.too_many_columns").format(len(line), Column.MAX))
        username = line[Column.USERNAME.value]
        UserCommand._validate_username_or_throw(username)
        for i in range(1, len(line)):
            logger.debug("column {}: {}".format(Column(i).name, line[i]))
            UserCommand._validate_item(line[i], CHOICES[i], Column(i))

    @staticmethod
    def _validate_item(item: str, possible_values: List[str], column_type) -> None:
        if item is None or item == "":
            # value can be empty for any column except user, which is checked elsewhere
            return
        if item in possible_values or possible_values == []:
            return
        raise AttributeError(_("tabcmd.report.error.generic_attribute").format(column_type, item))

    @staticmethod
    def get_users_from_file(csv_file: io.TextIOWrapper, logger=None) -> List[TSC.UserItem]:
        csv_file.seek(0)  # set to start of file in case it has been read earlier
        if logger:
            logger.debug("Reading from file {}".format(csv_file.name))
        user_list = []
        line = csv_file.readline()
        if logger:
            logger.debug("> {}".format(line))
        while line:
            user: Optional[TSC.UserItem] = UserCommand._parse_line(line)
            if user:
                user_list.append(user)
            line = csv_file.readline()
        return user_list

    @staticmethod
    def _parse_line(line: str) -> Optional[TSC.UserItem]:
        if line is None or line is False or line == "\n" or line == "":
            return None
        line = line.strip().lower()
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
    def act_on_users(
        logger: logging.Logger, server: object, action_name: str, server_method: Callable, args: argparse.Namespace
    ) -> None:

        group = None
        try:
            group = UserCommand.find_group(logger, server, args.name)
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(
                logger, _("errors.reportable.impersonation.group_not_found").format(args.name), exception=e
            )

        n_users_handled: int = 0
        number_of_errors: int = 0
        n_users_listed: int = UserCommand.validate_file_for_import(args.users, logger, strict=args.require_all_valid)
        logger.debug(_("importcsvsummary.line.processed").format(n_users_listed))

        error_list = []
        line_no = 0
        user_obj_list: List[TSC.UserItem] = UserCommand.get_users_from_file(args.users)
        logger.debug(_("tabcmd.result.success.parsed_users").format(len(user_obj_list)))
        for user_obj in user_obj_list:
            line_no += 1
            if not user_obj.name:
                number_of_errors += 1
                error_list.append(_("importcsvsummary.error.line").format(line_no, "No username", ""))
                continue

            try:
                username: str = user_obj.name
                user_id: str = UserCommand.find_user(logger, server, username).id
                logger.debug("{} user {} ({})".format(action_name, username, user_id))
            except TSC.ServerResponseError as e:
                number_of_errors += 1
                error_list.append(
                    _("importcsvsummary.error.line").format(line_no, username, "{}: {}".format(e.code, e.detail))
                )
                logger.debug(_("tabcmd.result.failure.user").format(username))
                continue

            try:
                server_method(group, user_id)
                n_users_handled += 1
                logger.info(_("tabcmd.result.success.user_actions").format(action_name, username, group))
            except TSC.ServerResponseError as e:
                number_of_errors += 1
                error_list.append(
                    _("importcsvsummary.error.line").format(line_no, username, "{}: {}".format(e.code, e.detail))
                )

        logger.info(_("session.monitorjob.percent_complete").format(100))
        logger.info(_("importcsvsummary.errors.count").format(number_of_errors))
        if number_of_errors > 0:
            i = 0
            max_printing = 5
            logger.info(_("importcsvsummary.error.details"))
            while i < number_of_errors and i < max_printing:
                logger.info(error_list[i])
                i += 1
            if number_of_errors > max_printing:
                logger.info(_("importcsvsummary.error.too_many_errors"))
                logger.info(_("importcsvsummary.remainingerrors"))

