from commands.auth.session import *
from commands.project.create_project_command import *
from commands.project.delete_project_command import *
from commands.group.delete_group_command import *
from commands.group.create_group_command import *
from commands.user.create_users_command import *
from commands.user.delete_users_command import *
from commands.user.remove_users_command import *


class CommandsMap:
    commands_hash_map = {"login": "Session",
                         "createproject": "CreateProjectCommand",
                         "deleteproject": "DeleteProjectCommand",
                         "creategroup": "CreateGroupCommand",
                         "deletegroup": "DeleteGroupCommand",
                         "createuser": "CreateUserCommand",
                         "deleteuser": "DeleteUserCommand",
                         "removeuser": "RemoveUserCommand"}
