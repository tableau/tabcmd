from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class ListCommand(Server):
    """
    Command to return a list of content the user can access
    """

    # strings to move to string files
    local_strings = {
        "tabcmd_content_listing": "===== Listing {0} content for user {1}...",
        "tabcmd_listing_label_name": "NAME: {}",
        "tabcmd_listing_label_id": "ID: {}",
        "tabcmd_listing_label_owner": "OWNER: {}",
        "tabcmd_content_none": "No content found.",
    }

    name: str = "list"
    description: str = "List content items of a specified type"

    @staticmethod
    def define_args(list_parser):
        args_group = list_parser.add_argument_group(title=ListCommand.name)
        args_group.add_argument(
            "content", choices=["projects", "workbooks", "datasources", "flows"], help="View content"
        )
        
        format_group = list_parser.add_mutually_exclusive_group()
        # TODO: should this be saved directly to csv? 
        format_group.add_argument("--machine", action="store_true", help="Format output as csv for machine reading")
        
        data_group = list_parser.add_argument_group(title="Attributes to include")
        # data_group.add_argument("-i", "--id", action="store_true", help="Show item id") # default true
        data_group.add_argument("-n", "--name", action="store_true", help="Show item name") # default true
        data_group.add_argument("-o", "--owner", action="store_true", help="Show item owner")
        data_group.add_argument("-d", "--details", action="store_true", help="Show children of the item")
        data_group.add_argument("-a", "--address", action="store_true", help="Show web address of the item")

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        content_type = args.content

        try:
            logger.info(ListCommand.local_strings["tabcmd_content_listing"].format(content_type, session.username))

            if content_type == "projects":
                items = server.projects.all()
            elif content_type == "workbooks":
                items = server.workbooks.all()
            elif content_type == "datasources":
                items = server.datasources.all()
            elif content_type == "flows":
                items = server.flows.all()

            if not items or len(items) == 0:
                logger.info(ListCommand.local_strings["tabcmd_content_none"])
                exit(0)


            logger.info(ListCommand.show_header(args, content_type))
            for item in items:
                if args.machine:
                    id = item.id
                    name = ", " + item.name if args.name else ""
                    owner =", " + item.owner_id if args.owner else ""
                    url = ""
                    if args.address and content_type in ["workbooks, datasources"]:
                        url = item.content_url 
                    children = ListCommand.format_children_listing(args, server, content_type, item) if args.details else ""
                        
                else:
                    id = ListCommand.local_strings["tabcmd_listing_label_id"].format(item.id)
                    name = ", " + ListCommand.local_strings["tabcmd_listing_label_name"].format(item.name) if args.name else ""
                    owner = ", " + ListCommand.local_strings["tabcmd_listing_label_owner"].format(item.owner_id) if args.owner else ""
                    
                    url = ""
                    if args.address and content_type == "workbooks":
                        url = item.content_url 
                    children = ListCommand.format_children_listing(args, server, content_type, item) if args.details else ""
                
                logger.info("{0}{1}{2}{3}".format(id, name, owner, url, children))

            # TODO: do we want this line if it is csv output?                
            logger.info("{} total {}".format(len(items), content_type))
        except Exception as e:
            Errors.exit_with_error(logger, e)

    @staticmethod
    def format_children_listing(args, server, content_type, item):
        if args.details:
            if content_type == "workbooks":
                server.workbooks.populate_views(item)
                child_items = item.views[:10]
                children = ", VIEWS: [" + ", ".join(map(lambda x: x.name, child_items)) + "]"
                return children
        return ""
            
    @staticmethod
    def show_header(args, content_type):
        id = "ID"
        name = ", NAME" if args.name else ""
        owner = ", OWNER" if args.owner else ""
        url = ", URL" if args.address and content_type in ["workbooks, datasources"] else ""
        children = ", CHILDREN" if args.details and content_type == "workbooks" else ""
        return "{0}{1}{2}{3}".format(id, name, owner, children)
        
