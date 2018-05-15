from guerillo.classes.backend_objects.backend_object import BackendObject


class HomeownerSearchResult(BackendObject):

    def __init__(self, uid=None, query=None, homeowners=None, pyres=None, pyre=None):
        super().__init__(uid)
        if pyres is None and pyre is None:
            self.homeowners = homeowners
            self.num_results = len(self.homeowners)
            self.query = query
        else:
            self.from_dictionary(pyres=pyres, pyre=pyre)

    def clean(self):
        indices_to_remove = list()
        for (i, homeowner) in enumerate(self.homeowners):
            if not homeowner.address:
                indices_to_remove.append(i)
            try:
                float(homeowner.mortgage_amount)
                float(homeowner.property_sale)
            except ValueError:
                indices_to_remove.append(i)

        for index in reversed(indices_to_remove):
            self.homeowners.pop(index)

        self.num_results = len(self.homeowners)

        return len(indices_to_remove)

    def clean_final_list(self, main_list):
        bad_eggs = []
        for i, entry in enumerate(main_list):
            if i != 0:
                if entry[1] == "":
                    bad_eggs.append(i)
                try:
                    float(entry[3])
                except ValueError:
                    bad_eggs.append(i)
        for bad_egg in reversed(bad_eggs):
            main_list.pop(bad_egg)
        header_row = main_list.pop(0)
        main_list.sort(key=lambda x: float(x[3]), reverse=True)
        main_list.insert(0, header_row)

    def from_dictionary(self, pyres=None, pyre=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre)
        self.num_results = dictionary["num_results"]

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

        header_row = homeowner_list.pop(0)
        homeowner_list.sort(key=lambda x: float(x[3]), reverse=True)
        homeowner_list.insert(0, header_row)

        return homeowner_list

