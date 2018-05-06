from guerillo.utils.state_codifier.state_codifier import StateCodifier


class Sanitizer:

    @staticmethod
    def state_name(state_name, abbrev=True):
        if StateCodifier.is_valid_state(state_name):
            if abbrev and StateCodifier.is_not_abbreviated(state_name):
                return StateCodifier.get_state_abbreviation(state_name)
            if not abbrev and StateCodifier.is_abbreviated(state_name):
                return StateCodifier.get_state_name(state_name)

            return state_name
        else:
            return None

    @staticmethod
    def county_name(county_name, ending=False):
        # TODO - Check against all county names to validate
        if county_name is not None:
            if ending and not county_name.endswith(" County"):
                return county_name + " County"

            if not ending and county_name.endswith(" County"):
                return county_name.replace(" County", "")

            return county_name
        else:
            return None

    @staticmethod
    def general_name(name, comma=True):
        if comma:
            return name.split(" ")[0] + ", " + name.split(" ")[1]
        else:
            return name.replace(",", "")

    @staticmethod
    def date(date):
        return date.replace("/", "")

    @staticmethod
    def date_time(date_time):
        return date_time.replace(":", "").replace(".", "-")
