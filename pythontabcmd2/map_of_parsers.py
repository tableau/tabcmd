from .parsers.create_project_parser import *


class ParsersMap:
    parsers_hashmap = {"createproject": CreateProjectParser.create_project_parser,
                       }
