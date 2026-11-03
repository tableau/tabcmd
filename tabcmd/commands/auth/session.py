import getpass
import json
import logging
import os

import requests
import tableauserverclient as TSC
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse, urlunparse

from tabcmd.version import version
from tabcmd.commands.constants import Errors
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log

from typing import Dict, Any, Optional


class Session:
    """
    Session class handles all authentication related work
    """

    TOKEN_CRED_TYPE = "token"
    PASSWORD_CRED_TYPE = "password"

    def __init__(self):
        self.username: Optional[str] = None
        # we don't store the password
        self.user_id: Optional[str] = None
        self.auth_token: Optional[str] = None
        self.token_name: Optional[str] = None
        self.token_value: Optional[str] = None
        self.password_file: Optional[str] = None
        self.token_file: Optional[str] = None
        self.site_name: Optional[str] = None  # The site name, e.g 'alpodev'
        self.site_id: Optional[str] = None  # The site id, e.g 'abcd-1234-1234-1244-1234'
        self.server_url: Optional[str] = None
        self.last_login_using: Optional[str] = None
        # server and site the saved auth token belongs to; set when the session file is read
        self._saved_server_url: Optional[str] = None
        self._saved_site_name: Optional[str] = None

        self.no_prompt: bool = False
        self.certificate: Optional[str] = None
        self.no_certcheck: bool = False
        self.no_proxy: bool = False
        self.proxy: Optional[str] = None
        self.timeout: Optional[int] = None

        self.logging_level: str = "info"
        self.logger = log(__name__, self.logging_level)  # instantiate here mostly for tests
        self._read_from_json()
        self.tableau_server: Optional[TSC.Server] = None  # this one is an object that doesn't get persisted in the file

    # called before we connect to the server
    # generally, we don't want to overwrite stored data with nulls
    def _update_session_data(self, args):
        # user id and site id are never passed in as args
        # last_login_using and tableau_server are internal data
        # self.command = args.???
        self.username = args.username or self.username or ""
        self.username = self.username.lower()
        server_base_url = self._get_server_base_url(args.server) if args.server else None
        self.server_url = server_base_url or self.server_url or "http://localhost"
        self.server_url = self.server_url.lower()
        if args.server is not None:
            self.site_name = None
        self.site_name = args.site_name or self.site_name or ""
        # site content URLs are case-sensitive, so the name is kept as given
        if self.site_name.lower() == "default":
            self.site_name = ""
        self.logging_level = args.logging_level or self.logging_level
        self.password_file = args.password_file or self.password_file
        self.token_file = args.token_file or self.token_file
        self.token_name = args.token_name or self.token_name
        self.token_value = args.token_value or self.token_value

        self.no_prompt = args.no_prompt  # have to set this on every call?
        self.certificate = args.certificate or self.certificate
        self.no_certcheck = args.no_certcheck  # have to set this on every call?
        self.no_proxy = args.no_proxy  # have to set this on every call?
        self.proxy = args.proxy or self.proxy
        self.timeout = self.timeout_as_integer(self.logger, args.timeout, self.timeout)

    @staticmethod
    def timeout_as_integer(logger, option_1, option_2):
        result = None
        if option_1:
            try:
                result = int(option_1)
            except Exception:
                result = 0
        if option_2 and (not result or result <= 0):
            try:
                result = int(option_2)
            except Exception:
                result = 0
        if not option_1 and not option_2:
            logger.debug(_("setsetting.status").format("timeout", "None"))
        elif not result or result <= 0:
            logger.warning(_("sessionoptions.errors.bad_timeout").format("--timeout", result))
        return result if result and result > 0 else 0

    @staticmethod
    def _read_password_from_file(filename, logger=None):
        _logger = logger or logging.getLogger(__name__)
        credential = None
        try:
            with open(str(filename), "r") as file_contents:
                reader = file_contents.readlines()
                for row in reader:
                    credential = row.rstrip("\r\n")
        except IOError as e:
            Errors.exit_with_error(
                _logger,
                message=_("session.errors.password_file_not_found").format(filename),
                exception=e,
            )
        return credential

    def _allow_prompt(self):
        try:
            return not self.no_prompt
        except Exception:
            return True

    def _create_new_credential(self, password, credential_type):
        if password is None:
            if self.password_file:
                if not os.path.isfile(self.password_file):
                    Errors.exit_with_error(
                        self.logger,
                        message=_("session.errors.password_file_not_found").format(self.password_file),
                    )
                password = Session._read_password_from_file(self.password_file, self.logger)
                if not password:
                    Errors.exit_with_error(self.logger, _("session.errors.missing_arguments").format(""))
            elif self._allow_prompt():
                password = getpass.getpass(_("session.password"))
            else:
                Errors.exit_with_error(self.logger, _("session.errors.script_no_password"))

        if credential_type == Session.PASSWORD_CRED_TYPE and self.username and password:
            credentials = TSC.TableauAuth(self.username, password, site_id=self.site_name)
            self.last_login_using = "username"
            return credentials
        elif credential_type == Session.TOKEN_CRED_TYPE and self.token_name:
            credentials = self._create_new_token_credential()
            return credentials
        else:
            Errors.exit_with_error(self.logger, _("session.errors.missing_arguments").format(""))

    def _create_new_token_credential(self):
        if self.token_value:
            token = self.token_value
        elif self.token_file:
            if not os.path.isfile(self.token_file):
                Errors.exit_with_error(
                    self.logger,
                    message=_("session.errors.token_file_not_found").format(self.token_file),
                )
            token = Session._read_password_from_file(self.token_file, self.logger)
            if not token:
                Errors.exit_with_error(self.logger, _("session.errors.missing_arguments").format("token"))
        elif self._allow_prompt():
            token = getpass.getpass("Token:")
        else:
            Errors.exit_with_error(self.logger, _("session.errors.missing_arguments").format("token"))

        if self.token_name and token:
            credentials = TSC.PersonalAccessTokenAuth(self.token_name, token, site_id=self.site_name)
            self.last_login_using = "token"
            return credentials
        else:
            Errors.exit_with_error(self.logger, _("session.errors.missing_arguments").format("token name"))

    @staticmethod
    def _redact_proxy(proxy: Optional[str]) -> Optional[str]:
        """Hide any user:password embedded in a proxy URL before it is logged."""
        if not proxy or "@" not in proxy:
            return proxy
        scheme, sep, rest = proxy.rpartition("://")
        host_part = rest.rsplit("@", 1)[1]
        return "{}{}***@{}".format(scheme, sep, host_part)

    @staticmethod
    def _redact_http_options(http_options: Dict[str, Any]) -> Dict[str, Any]:
        redacted = dict(http_options)
        proxies = redacted.get("proxies")
        if proxies:
            redacted["proxies"] = {k: Session._redact_proxy(v) for k, v in proxies.items()}
        return redacted

    def _open_connection_with_opts(self) -> TSC.Server:
        self.logger.debug("Setting up request options")
        http_options: Dict[str, Any] = {"headers": {"User-Agent": "Tabcmd/{}".format(version)}}

        if self.no_certcheck:
            http_options["verify"] = False
            urllib3.disable_warnings(category=InsecureRequestWarning)

        # Not validating the proxy format (old tabcmd did, with sessionoptions.errors.bad_proxy_format):
        # requests reports a bad proxy itself.
        if self.proxy:
            self.logger.debug("Setting http proxy: {}".format(self._redact_proxy(self.proxy)))
            proxies = {"http": self.proxy, "https": self.proxy}
            http_options["proxies"] = proxies
        if self.no_proxy:
            # override any proxy that was set
            http_options["proxies"] = None

        if self.timeout:
            http_options["timeout"] = self.timeout

        if self.certificate:
            http_options["cert"] = self.certificate

        try:
            self.logger.debug(self._redact_http_options(http_options))
            # this is the only place we open a connection to the server
            # so the request options are all set for the session now
            tableau_server = TSC.Server(self.server_url, http_options=http_options)

        except Exception as e:
            self.logger.debug(
                "Connection args: server {}, site {}, proxy {}/no-proxy {}, cert {}".format(
                    self.server_url, self.site_name, self._redact_proxy(self.proxy), self.no_proxy, self.certificate
                )
            )
            Errors.exit_with_error(self.logger, "Failed to connect to server", e)

        self.logger.debug("Finished setting up connection")
        return tableau_server

    def _verify_server_connection_unauthed(self):
        assert self.tableau_server is not None  # Type hint for mypy
        try:
            self.tableau_server.use_server_version()
        except requests.exceptions.ReadTimeout as timeout_error:
            Errors.exit_with_error(
                self.logger,
                message="Timed out after {} seconds attempting to connect to server".format(self.timeout),
                exception=timeout_error,
            )
        except requests.exceptions.RequestException as requests_error:
            Errors.exit_with_error(
                self.logger, message="Error attempting to connect to the server", exception=requests_error
            )
        except Exception as e:
            Errors.exit_with_error(self.logger, exception=e)

    def _create_new_connection(self) -> TSC.Server:
        self._print_server_info()
        self.logger.info(_("session.connecting"))
        try:
            self.tableau_server = self._open_connection_with_opts()
        except Exception as e:
            Errors.exit_with_error(self.logger, "Failed to connect to server", exception=e)

        assert self.tableau_server is not None  # Type hint for mypy
        return self.tableau_server

    def _print_server_info(self):
        self.logger.info("=====   Server: {}".format(self.server_url))
        if self.proxy:
            self.logger.info("=====   Proxy: {}".format(self._redact_proxy(self.proxy)))
        if self.username:
            self.logger.info("=====   Username: {}".format(self.username))
        if self.token_name:
            self.logger.info("=====   Token Name: {}".format(self.token_name))
        if self.certificate:
            self.logger.info("=====   Certificate: {}".format(self.certificate))
        site_display_name = self.site_name or "Default Site"
        self.logger.info(_("dataconnections.classes.tableau_server_site") + ": {}".format(site_display_name))

    # side-effect: sets self.username
    def _validate_existing_signin(self):
        # when do these two messages show up? self.logger.info(_("session.auto_site_login"))
        try:
            if self.tableau_server and self.tableau_server.is_signed_in() and self.user_id:
                server_user = self.tableau_server.users.get_by_id(self.user_id).name
                if not self.username:
                    self.logger.info("Fetched user details from server")
                    self.username = server_user

                return self.tableau_server
        except TSC.ServerResponseError as e:
            self.logger.info(_("publish.errors.unexpected_server_response").format(e))
        except Exception as e:
            self.logger.info(_("errors.internal_error.request.message").format(e))
        return None

    # server connection created, not yet logged in
    def _sign_in(self, tableau_auth) -> TSC.Server:
        if not self.tableau_server:
            Errors.exit_with_error(self.logger, "No server connection available for sign in")

        self.logger.debug(_("session.login") + (self.server_url or ""))
        self.logger.debug(_("listsites.output").format("", self.username or self.token_name, self.site_name))
        assert self.tableau_server is not None  # Type hint for mypy
        try:
            self.tableau_server.auth.sign_in(tableau_auth)  # it's the same call for token or user-pass
        except Exception as e:
            Errors.exit_with_error(self.logger, exception=e)
        try:
            self.site_id = self.tableau_server.site_id
            self.user_id = self.tableau_server.user_id
            self.auth_token = self.tableau_server.auth_token
            success = self._validate_existing_signin()
        except Exception as e:
            Errors.exit_with_error(self.logger, exception=e)
        if success:
            self.logger.info(_("common.output.succeeded"))
        else:
            Errors.exit_with_error(self.logger, message="Sign in failed")

        return self.tableau_server

    def _get_saved_credentials(self):
        if self.last_login_using == "username":
            credentials = self._create_new_credential(None, Session.PASSWORD_CRED_TYPE)
        elif self.last_login_using == "token":
            credentials = self._create_new_token_credential()
        else:
            return None

        return credentials

    def _restore_saved_session(self) -> Optional[TSC.Server]:
        # Fixes #463: without this, tabcmd <cmd> after a successful `tabcmd login`
        # falls into _get_saved_credentials() -> getpass.getpass() and hangs silently
        # in any non-TTY context. Reattach to the token saved in tableau_auth.json instead.
        if not (self.auth_token and self.site_id and self.user_id and self.server_url):
            return None
        # The saved token is only valid for the server and site it was issued on. If
        # --server or --site point elsewhere, reusing it would run the command against
        # the previously logged-in site.
        if (self.server_url or "") != (self._saved_server_url or "") or (self.site_name or "") != (
            self._saved_site_name or ""
        ):
            self.logger.debug("Saved session is for a different server or site; will re-authenticate")
            return None
        try:
            server = self._open_connection_with_opts()
        except (Exception, SystemExit) as e:
            # _open_connection_with_opts reports failures through exit_with_error, which raises
            # SystemExit, so that has to be caught for the fallback to happen.
            # Log the exception class only; the message can include the request URL and
            # in some code paths downstream would echo request bodies. Class name is
            # enough for a fallback-diagnostic breadcrumb.
            self.logger.debug("Could not open connection to reuse saved session ({})".format(type(e).__name__))
            return None
        try:
            server._set_auth(self.site_id, self.user_id, self.auth_token)
            # use_server_version negotiates the REST API version TSC hard-codes into
            # subsequent endpoint URLs; required, not merely informational.
            server.use_server_version()
            # Probe a user-scoped endpoint so an expired token surfaces here rather
            # than later inside a publish() body.
            server.users.get_by_id(self.user_id)
        except Exception as e:
            # See note above: exception class only, no str(e).
            self.logger.debug("Saved auth token no longer valid ({}); will re-authenticate".format(type(e).__name__))
            return None
        # Match tabcmd classic's on-reuse banner (Continuing previous session + server info)
        # so users retain visual confirmation of which server/site each subcommand hits.
        self.logger.info(_("session.continuing_session"))
        self._print_server_info()
        self.tableau_server = server
        return server

    # external entry point:
    def create_session(self, args, logger):
        signed_in_object = None
        # cached info from json was loaded in __init__; overwrite with new args if available
        self._update_session_data(args)
        self.logger = logger or log(self.__class__.__name__, self.logging_level)

        credentials = None
        if args.password or args.password_file:
            self._end_session()
            # we don't save the password anywhere, so we pass it along directly
            credentials = self._create_new_credential(args.password, Session.PASSWORD_CRED_TYPE)
        elif args.token_value or args.token_file:
            self._end_session()
            credentials = self._create_new_token_credential()
        elif args.username and not self.tableau_server:
            # username given but no password/token and no active session: prompt for password
            credentials = self._create_new_credential(None, Session.PASSWORD_CRED_TYPE)
        else:  # no login arguments given - look for saved info
            # maybe we're already signed in!
            if self.tableau_server:
                self.logger.info(_("session.continuing_session"))
                signed_in_object = self._validate_existing_signin()

            # Reattach to the token saved on disk by an earlier `tabcmd login`
            # before falling back to _get_saved_credentials, which would prompt
            # for a password we don't have. Fixes #463.
            if not signed_in_object:
                signed_in_object = self._restore_saved_session()

            if not signed_in_object:
                credentials = self._get_saved_credentials()

        if credentials and not signed_in_object:
            self.logger.debug("Signin details found:")
            self.tableau_server = self._create_new_connection()
            self._verify_server_connection_unauthed()
            signed_in_object = self._sign_in(credentials)

        if not signed_in_object:
            message = "Run 'tabcmd login -h' for details on required arguments"
            Errors.exit_with_error(self.logger, _("session.errors.missing_arguments").format(message))
        if args.no_cookie:
            self._remove_json()
        else:
            self._save_session_to_json()
        return signed_in_object

    def end_session_and_clear_data(self):
        # A live connection signs out its own token. Otherwise (the usual case: each command
        # is a new process) invalidate the token saved on disk.
        had_live_session = self.tableau_server is not None
        self._end_session()
        if not had_live_session:
            self._sign_out_saved_token()
        self.logger.info(_("session.logout"))
        self._clear_data()

    def _sign_out_saved_token(self):
        # Each command runs in a new process, so the session being logged out is the
        # token saved on disk, not a live connection. Invalidate it on the server too;
        # failing to do so must not stop the local cleanup.
        if not (self.auth_token and self.site_id and self.user_id and self.server_url):
            return
        try:
            server = self._open_connection_with_opts()
            server._set_auth(self.site_id, self.user_id, self.auth_token)
            server.use_server_version()
            server.auth.sign_out()
        except (Exception, SystemExit) as e:
            self.logger.debug("Could not sign out saved session on the server ({})".format(type(e).__name__))

    def _end_session(self):
        if self.tableau_server:
            self.tableau_server.auth.sign_out()
            self.tableau_server = None

    def _clear_data(self):
        self._remove_json()
        self.username = None
        self.user_id = None
        self.auth_token = None
        self.token_name = None
        self.token_value = None
        self.site_name = None
        self.site_id = None
        self.server_url = None
        self._saved_server_url = None
        self._saved_site_name = None
        self.last_login_using = None
        self.password_file = None
        self.token_file = None

        self.tableau_server = None

        self.certificate = None
        self.no_certcheck = False
        self.no_proxy = False
        self.proxy = None
        self.timeout = None

    # json file functions ----------------------------------------------------
    # These should be moved into a separate class
    def _get_file_path(self):
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, "tableau_auth.json")
        return file_path

    def _read_from_json(self):
        if not self._json_exists():
            return
        file_path = self._get_file_path()
        content = None
        try:
            with open(str(file_path), "r") as file_contents:
                data = json.load(file_contents)
                if data is None or data == {}:
                    return
                content = data["tableau_auth"]
                if content is None:
                    return
                self._save_data_from_json(content)
        except json.JSONDecodeError as e:
            self._wipe_bad_json(e, "Error reading data from session file")
        except IOError as e:
            self._wipe_bad_json(e, "Error reading session file")
        except AttributeError as e:
            self._wipe_bad_json(e, "Error parsing session details from file")
        except Exception as e:
            self._wipe_bad_json(e, "Unexpected error reading session details from file")

    def _save_data_from_json(self, content):
        try:
            auth = content[0]
            if auth is None:
                self._wipe_bad_json(ValueError(), "Empty session file")
                return
            # .get: a file written by another version may lack newer keys; don't discard the session over it
            self.auth_token = auth.get("auth_token")
            self.server_url = auth.get("server")
            self.site_name = auth.get("site_name")
            self._saved_server_url = self.server_url
            self._saved_site_name = self.site_name
            self.site_id = auth.get("site_id")
            self.username = auth.get("username")
            self.user_id = auth.get("user_id")
            self.token_name = auth.get("personal_access_token_name")
            self.token_value = auth.get("personal_access_token")
            self.last_login_using = auth.get("last_login_using")
            self.password_file = auth.get("password_file")
            self.token_file = auth.get("token_file")
            self.no_prompt = bool(auth.get("no_prompt"))
            self.no_certcheck = bool(auth.get("no_certcheck"))
            self.certificate = auth.get("certificate")
            self.no_proxy = bool(auth.get("no_proxy"))
            self.proxy = auth.get("proxy")
            self.timeout = auth.get("timeout")
        except AttributeError as e:
            self._wipe_bad_json(e, "Unrecognized attribute in session file")
        except Exception as e:
            self._wipe_bad_json(e, "Failed to load session file")

    def _wipe_bad_json(self, e, message):
        self.logger.debug(message + ": " + e.__str__())
        self.logger.info(_("session.new_session"))
        self._remove_json()

    def _json_exists(self):
        # todo: make this location configurable
        return os.path.exists(self._get_file_path())

    def _save_session_to_json(self):
        try:
            data = self._serialize_for_save()
            self._save_file(data)
        except Exception as e:
            self._wipe_bad_json(e, "Failed to save session file")

    def _save_file(self, data: Dict[str, Any]) -> None:
        file_path = str(self._get_file_path())
        # The file holds the auth token and any personal access token secret: keep it
        # readable by the owner only. The mode applies when the file is created; chmod
        # tightens a file left behind with looser permissions by an earlier version.
        fd = os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            os.chmod(file_path, 0o600)
        except OSError:
            self.logger.debug("Could not restrict permissions on the session file")
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)

    def _serialize_for_save(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"tableau_auth": []}
        data["tableau_auth"].append(
            {
                "auth_token": self.auth_token,
                "server": self.server_url,
                "username": self.username,
                "user_id": self.user_id,
                "site_name": self.site_name,
                "site_id": self.site_id,
                "personal_access_token_name": self.token_name,
                "personal_access_token": self.token_value,
                "last_login_using": self.last_login_using,
                "password_file": self.password_file,
                "token_file": self.token_file,
                "no_prompt": self.no_prompt,
                "no_certcheck": self.no_certcheck,
                "certificate": self.certificate,
                "no_proxy": self.no_proxy,
                "proxy": self.proxy,
                "timeout": self.timeout,
            }
        )
        return data

    def _remove_json(self):
        file_path = ""
        try:
            if not self._json_exists():
                return
            file_path = self._get_file_path()
            self._save_file({})
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            message = "Error clearing session data from {}: check and remove manually".format(file_path)
            self.logger.error(message)
            self.logger.error(e)

    def _get_server_base_url(self, url: str):
        try:
            # Without "://", urlparse reads "host:8080" as scheme "host", so add the
            # default scheme before parsing.
            if "://" not in url:
                url = "https://" + url
            parsed = urlparse(url)
            # Keep only scheme and host[:port]; any path is discarded
            return urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))
        except Exception as e:
            Errors.exit_with_error(self.logger, exception=e)
