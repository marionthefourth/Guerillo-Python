from datetime import datetime

from guerillo.classes.backend_objects.backend_object import BackendObject, BackendType
from guerillo.utils.sanitizer import Sanitizer


class SearchQuery(BackendObject):
    b_type = BackendType.SEARCH_QUERY

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
            self.user_uid = user_uid
            self.county_uid = county_uid
        else:
            self.end_date = inputs[3]
            self.start_date = inputs[2]
            self.upper_bound = inputs[1]
            self.lower_bound = inputs[0]

    def __str__(self):
        return super().__str__() + "- LB: " + self.lower_bound + ", UB: " + self.upper_bound + ", SD: " + \
               self.start_date + ", ED: " + self.end_date

    def validate_number_bounds(self):
        sanitized_lower_bound = Sanitizer.numeric_bound(self.lower_bound, full=False)
        sanitized_upper_bound = Sanitizer.numeric_bound(self.upper_bound, full=False)

        try:
            float(sanitized_lower_bound)
        except ValueError:
            return False, "Minimum mortgage amount must be a positive whole number"

        try:
            float(sanitized_upper_bound)
        except ValueError:
            return False, "Maximum mortgage amount must be a non-zero whole number"

        sanitized_upper_bound = float(sanitized_upper_bound)
        sanitized_lower_bound = float(sanitized_lower_bound)
        self.lower_bound = Sanitizer.numeric_bound(sanitized_lower_bound, full=True)
        self.upper_bound = Sanitizer.numeric_bound(sanitized_upper_bound, full=True)

        if sanitized_lower_bound <= 0:
            return False, "Minimum mortgage amount must be a positive whole number"

        if sanitized_upper_bound <= 0:
            return False, "Maximum mortgage amount must be a positive non-zero whole number"

        if sanitized_lower_bound >= sanitized_upper_bound:
            return False, "Maximum mortgage must be greater than minimum amount"

        return True, "All number bounds are valid"

    def validate_date_bounds(self):
        sanitized_start_date = Sanitizer.date_bound(self.start_date)
        sanitized_end_date = Sanitizer.date_bound(self.end_date)

        self.start_date = sanitized_start_date
        self.end_date = sanitized_end_date

        try:
            self.start_date = datetime.strptime(self.start_date, "%m/%d/%Y").strftime('%m/%d/%Y')
        except ValueError:
            return False, "Start Date must be in the format MM/DD/YYYY"

        try:
            self.end_date = datetime.strptime(self.end_date, "%m/%d/%Y").strftime('%m/%d/%Y')
        except ValueError:
            return False, "End Date must be in the format MM/DD/YYYY"

        for i, date in enumerate(self.end_date.split("/")):
            if self.start_date.split("/")[i] > date:
                return False, "Start Date must be on or before the End Date"

        return True, "All date bounds are valid"

    def sanitize(self):
        self.lower_bound = Sanitizer.numeric_bound(self.lower_bound, full=False)
        self.upper_bound = Sanitizer.numeric_bound(self.upper_bound, full=False)

    def desanitize(self):
        self.lower_bound = Sanitizer.numeric_bound(self.lower_bound, full=True)
        self.upper_bound = Sanitizer.numeric_bound(self.upper_bound, full=True)

    def validate(self):
        if not self.validate_number_bounds()[0]:
            return self.validate_number_bounds()

        if not self.validate_date_bounds()[0]:
            return self.validate_date_bounds()

        return True, "All values are valid"

    def is_valid(self):
        return self.validate()[0]

    def invalid_message(self):
        return self.validate()[1]

    def from_dictionary(self, pyres=None, pyre=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre)
        self.lower_bound = dictionary["lower_bound"]
        self.upper_bound = dictionary["upper_bound"]
        self.start_date = dictionary["start_date"]
        self.end_date = dictionary["end_date"]
