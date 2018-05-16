from enum import Enum

from guerillo.backend.backend import Backend


class BackendType(Enum):
    USER = "User"
    LOCK = "Lock"
    AUX = "Auxiliary"
    COUNTY = "County"
    DEFAULT = "Default"
    KEYCHAIN = "Keychain"
    SEARCH_QUERY = "SearchQuery"
    REQUEST_QUEUE = "RequestQueue"
    HOMEOWNER_SEARCH_RESULT = "HomeownerSearchResult"

    def is_auxiliary(self):
        return self == BackendType.AUX or self == BackendType.KEYCHAIN or\
            self == BackendType.REQUEST_QUEUE or self == BackendType.LOCK


class BackendObject:

    b_type = BackendType.DEFAULT

    def __init__(self, uid=None):
        if uid is not None:
            self.uid = uid
        else:
            self.generate_uid()

    def __repr__(self):
        return self.b_type.__str__() + ": "

    def __str__(self):
        return self.b_type.__str__() + ": "

    def generate_uid(self):
        self.uid = Backend.get().database().generate_key()

    @staticmethod
    def pyres_to_dictionary(pyres=None, pyre=None):
        dictionary = dict()
        if pyres and pyres.pyres:
            for item in pyres.pyres:
                dictionary[item.item[0]] = item.item[1]
        elif pyre is not None:
            dictionary = pyre.item[1]
        else:
            return None

        return dictionary

    def from_dictionary(self, pyres=None, pyre=None):
        dictionary = BackendObject.pyres_to_dictionary(pyres=pyres, pyre=pyre)
        if dictionary:
            self.uid = dictionary["uid"]
            return dictionary
        else:
            return None

    def to_dictionary(self):
        return {
            "uid": self.uid
        }
