from datetime import datetime

from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.auxiliary_object import AuxiliaryObject
from guerillo.classes.backend_objects.backend_object import BackendType
from guerillo.classes.backend_objects.searches.search import Search, SearchType
from guerillo.utils.sanitizer import Sanitizer


class Query(Search):
    b_type = BackendType.QUERY
    """ The SearchQuery is part 1/3 dealing with Searches 
            SearchQuery is created & filled with their user_uid and date/mortgage bounds,and the county uid searched
            It is then auto-populated with a timestamp, uid, result_uid (for client data updates)
    """

    def __init__(self, start_date=None, end_date=None, lower_bound=None, upper_bound=None,
                 uid=None, user_uid=None, pyres=None, pyre=None, message_data=None,
                 county_uid_list=None, inputs=None, twin_uid=None):
        super().__init__(uid, user_uid, twin_uid)

        self.timestamp = datetime.now()
        self.county_uid_list = county_uid_list if county_uid_list else list()

        if pyres or pyre or message_data:
            self.from_dictionary(pyres=pyres, pyre=pyre, message_data=message_data)
        else:
            self.end_date = end_date if not inputs else inputs[3]
            self.start_date = start_date if not inputs else inputs[2]
            self.lower_bound = lower_bound if not inputs else inputs[0]
            self.upper_bound = upper_bound if not inputs else inputs[1]

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

        if sanitized_lower_bound < 0:
            return False, "Minimum mortgage amount must be a positive whole number"

        if sanitized_upper_bound <= 0:
            return False, "Maximum mortgage amount must be a positive non-zero whole number"

        if sanitized_lower_bound >= sanitized_upper_bound:
            return False, "Maximum mortgage must be greater than minimum amount"

        return True, "All number bounds are valid"

    def validate_date_bounds(self):
        sanitized_end_date = Sanitizer.date_bound(self.end_date)
        sanitized_start_date = Sanitizer.date_bound(self.start_date)

        self.end_date = sanitized_end_date
        self.start_date = sanitized_start_date

        try:
            self.start_date = datetime.strptime(self.start_date, "%m/%d/%Y").strftime('%m/%d/%Y')
        except ValueError:
            return False, "Start Date must be in the format MM/DD/YYYY"

        try:
            self.end_date = datetime.strptime(self.end_date, "%m/%d/%Y").strftime('%m/%d/%Y')
        except ValueError:
            return False, "End Date must be in the format MM/DD/YYYY"

        YEAR = 2
        MONTH = 0
        DAY = 1

        if self.start_date.split("/")[YEAR] < self.end_date.split("/")[YEAR]:
            return True, "All date bounds are valid"
        elif self.start_date.split("/")[YEAR] == self.end_date.split("/")[YEAR]:
            if self.start_date.split("/")[MONTH] < self.end_date.split("/")[MONTH]:
                return True, "All date bounds are valid"
            elif self.start_date.split("/")[MONTH] == self.end_date.split("/")[MONTH]:
                if self.start_date.split("/")[DAY] <= self.end_date.split("/")[DAY]:
                    return True, "All date bounds are valid"

        return False, "Start Date must be on or before the End Date"

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

    def pause(self):
        super().pause()
        search_result = Backend.read(BackendType.RESULT, self.twin_uid)
        search_result.pause()

    def resume(self):
        super().resume()
        search_result = Backend.read(BackendType.RESULT, self.twin_uid)
        search_result.resume()

    def stop(self):
        super().stop()
        search_result = Backend.read(BackendType.RESULT, self.twin_uid)
        search_result.stop()

    def update(self):
        super().update()
        search_result = Backend.read(BackendType.RESULT, self.twin_uid)
        search_result.update()

    def is_valid(self):
        return self.validate()[0]

    def invalid_message(self):
        return self.validate()[1]

    def from_dictionary(self, pyres=None, pyre=None, message_data=None):
        dictionary = super().from_dictionary(pyres, pyre, message_data)
        if dictionary:
            self.end_date = dictionary.get("end_date", None)
            self.timestamp = dictionary.get("timestamp", None)
            self.start_date = dictionary.get("start_date", None)
            self.county_uid_list = AuxiliaryObject.get_uid_list_from_dictionary(self, dictionary, v_index=0)

            if self.s_type == SearchType.HOMEOWNER:
                self.lower_bound = dictionary.get("minimum_mortgage_amount", None)
                self.upper_bound = dictionary.get("maximum_mortgage_amount", None)
        return dictionary

    def to_dictionary(self):
        main_dict = {
            **super().to_dictionary(),
            "end_date": self.end_date,
            "start_date": self.start_date,
            "timestamp": str(self.timestamp),
            **self.get_type_specific_elements()
        }
        if self.county_uid_list:
            return {
                ** main_dict,
                ** AuxiliaryObject.get_uid_dictionary_from_uid_list(self, self.county_uid_list, v_index=0)
            }
        else:
            return main_dict

    def get_type_specific_elements(self):
        if self.s_type == SearchType.HOMEOWNER:
            return {
                "minimum_mortgage_amount": self.lower_bound,
                "maximum_mortgage_amount": self.upper_bound,
            }
        return dict()
