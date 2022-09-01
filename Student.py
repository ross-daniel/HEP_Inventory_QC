# --------------------------------------------------------------------------------------------
#
#       Student Class for CSU HEP Lab Inventory System, holds student employee info
#
#                              created by: Ross Stauder
#                                   rev: July 2022
#                     DUNE - Deep Underground Neutrino Experiment
# --------------------------------------------------------------------------------------------

class Student:
    def __init__(self, csuid, ref):
        self.csuid = csuid
        self.users = ref.child('users').get()
        # Search the database for the given ID number
        for key in self.users:
            if key == self.csuid:
                self.name = self.users[key]
