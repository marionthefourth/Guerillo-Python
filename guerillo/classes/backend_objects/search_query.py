from guerillo.classes.backend_objects.backend_object import BackendObject, BackendType


class SearchQuery(BackendObject):

    type = BackendType.SEARCH_QUERY

    def __init__(self, start_date=None, end_date=None, lower_bound=None, upper_bound=None, uid=None, user_uid=None,
                 pyres=None, pyre=None, county_uid=None, inputs=None):
        super().__init__(uid=uid)
        if pyres or pyre:
            self.from_dictionary(pyres=pyres, pyre=pyre)
        elif not inputs:
            self.end_date = end_date
            self.start_date = start_date
            self.lower_bound = lower_bound
            self.upper_bound = upper_bound
        else:
            self.end_date = inputs[3]
            self.start_date = inputs[2]
            self.upper_bound = inputs[1]
            self.lower_bound = inputs[0]

        self.user_uid = user_uid
        self.county_uid = county_uid

    def from_dictionary(self, pyres=None, pyre=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre)
        self.lower_bound = dictionary["lower_bound"]
        self.upper_bound = dictionary["upper_bound"]
        self.start_date = dictionary["start_date"]
        self.end_date = dictionary["end_date"]
