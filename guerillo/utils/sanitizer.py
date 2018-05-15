import locale
from datetime import datetime

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
    def numeric_bound(amount, full=False):
        contains_dollar_sign = "$" in str(amount)
        contains_commas = "," in str(amount)

        if not full:
            if contains_dollar_sign:
                amount = str(amount).replace("$", "")

            if contains_commas:
                amount = str(amount).replace(",", "")
        else:
            amount = Sanitizer.numeric_bound(amount, full=False)
            locale.setlocale(locale.LC_ALL, '')
            amount = "${:,.2f}".format(float(amount))
        return amount

    @staticmethod
    def date_bound(date, full=False):
        contains_back_slashes = "\\" in date
        contains_dashes = "-" in date

        if contains_back_slashes:
            date = date.replace("\\", "/")
        if contains_dashes:
            date = date.replace("-", "/")

        return date

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
