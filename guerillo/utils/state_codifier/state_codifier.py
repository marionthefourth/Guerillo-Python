from guerillo.utils.state_codifier import abbreviation_to_name
from guerillo.utils.state_codifier import name_to_abbreviation


class StateCodifier:

    @staticmethod
    def get_state_abbreviation(state_name):
        return name_to_abbreviation.to_dictionary().get(state_name, None)

    @staticmethod
    def get_state_name(state_abbreviation):
        return abbreviation_to_name.to_dictionary().get(state_abbreviation, None)

    @staticmethod
    def is_abbreviated(state_name):
        if len(state_name) == 2:
            # Probably is abbreviated but lets double check
            return StateCodifier.get_state_name(state_name) is not None
        else:
            return False

    @staticmethod
    def is_not_abbreviated(state_name):
        if len(state_name) != 2:
            # Isn't abbreviated but could still be invalid
            return StateCodifier.get_state_abbreviation(state_name) is not None

    @staticmethod
    def is_valid_state(state_name):
        return state_name is not None and \
               (StateCodifier.is_abbreviated(state_name) or StateCodifier.is_not_abbreviated(state_name))
