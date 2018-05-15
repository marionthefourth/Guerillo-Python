from guerillo.classes.backend_objects.county import County
from guerillo.utils.file_storage import FileStorage
from guerillo.utils.sanitizer import Sanitizer


class CensusCountyAPI:

    @staticmethod
    def get_states_with_counties_dictionary(state_filter=None, county_filter=None):
        """ Read Text File Containing Data """
        text_file = FileStorage.read("national_county.txt")

        state_name = None
        county_list = list()
        states_with_counties_list = list()

        state_filter = Sanitizer.state_name(state_filter)
        county_filter = Sanitizer.county_name(county_filter)

        for line in text_file:
            """ Check State Abbreviation Against Previous Abbreviation """
            # if different or empty, has moved on to new state
            data = line.split(",")
            if state_name is None or state_name != data[0]:
                if state_name is not None and state_name != data[0] and county_list.__sizeof__() != 0:
                    # Store Abbrev., if County List Not Empty push List along with State Abbreviation into Dictionary
                    if state_filter is None or (state_filter is not None and state_filter == state_name):
                        states_with_counties_list.append({state_name, ', '.join(county_list)})

                    if state_filter is not None and state_filter == state_name:
                        # print(states_with_counties_list)
                        return states_with_counties_list

                    county_list = []

                if state_name != data[0] or state_name is None:
                    state_name = data[0]

            county_list.append(data[3].replace(" County", ""))

        # print(states_with_counties_list)
        return states_with_counties_list

    @staticmethod
    def get_counties(state_filter=None, county_filter=None):
        """ Read Text File Containing Data """
        text_file = FileStorage.read("national_county.txt")

        counties = list()

        state_filter = Sanitizer.state_name(state_filter)
        county_filter = Sanitizer.county_name(county_filter, ending=True)

        for line in text_file:
            """ Check State Abbreviation Against Previous Abbreviation """
            # if different or empty, has moved on to new state
            data = line.split(",")
            county = County(state_name=data[0], state_fips=data[1], county_fips=data[2], county_name=data[3])

            if state_filter is not None and state_filter == data[0]:
                if county_filter is None:
                    counties.append(county)
                    continue
                elif county_filter == data[3]:
                    return [county]

            if county_filter is not None and county_filter == data[3]:
                    if state_filter is None:
                        return ["Not Found"]
                    elif state_filter == data[0]:
                        return [county]

            if state_filter is None and county_filter is None:
                counties.append(county)

            print(county.to_dictionary())

        return counties

    @staticmethod
    def get_state_name(fips=None, county_name=None):
        text_file = FileStorage.read("national_county.txt")

        county_name = Sanitizer.county_name(county_name, ending=True)

        for line in text_file:
            data = line.split(",")

            if county_name is not None or fips is not None:
                if fips == data[1] + data[2] or county_name == data[3] and fips == data[1] + data[2]:
                    return data[0]

        return "Not found"

    @staticmethod
    def get_county_name(fips):
        text_file = FileStorage.read("national_county.txt")

        for line in text_file:
            data = line.split(",")
            if fips == data[1] + data[2]:
                return Sanitizer.county_name(data[3], ending=True)

        return "Not found"
