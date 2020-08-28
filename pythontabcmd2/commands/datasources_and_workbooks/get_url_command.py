# import tableauserverclient as TSC
# from .. import log
# from ... import Session
# from .. import GetUrlParser
#
#
# class GetUrl:
#     def __init__(self, args, schedule):
#         self.schedule = schedule
#         self.args = args
#         self.logging_level = args.logging_level
#         self.logger = log('pythontabcmd2.runschedule_command',
#                           self.logging_level)
#
#     @classmethod
#     def parse(cls):
#         args, schedule = GeturlpARSER.runschedule_parser()
#         return cls(args, schedule)
#
#     def run_command(self):
#         session = Session()
#         server_object = session.create_session(self.args)
#         self.run_schedule(server_object)
#
#     def run_schedule(self, server):
#         pass
