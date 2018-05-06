from guerillo.classes.backend_objects.backend_object import BackendObject


class HomeownerSearchResult(BackendObject):

    def __init__(self, uid=None, query=None, homeowners=None):
        super().__init__(uid)
        self.homeowners = homeowners
        self.query = query


    def to_dictionary(self):
        return {
            **super().to_dictionary(),
            **self.query.to_dictionary()
            ** {"num_results": len(self.homeowners)}
        }

    def to_list(self):
        homeowner_list = list()
        homeowner_list.append(["Name", "Address", "Date/Time", "Amount of Mortgage", "Property Sale Price"])
        for homeowner in self.homeowners:
            homeowner_list.append(homeowner.to_list())

        return homeowner_list

