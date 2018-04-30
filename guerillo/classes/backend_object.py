from enum import Enum

from guerillo.backend.backend import Backend


class BackendType(Enum):
    USER = "User"
    LOCK = "Lock"
    AUX = "Auxiliary"
    COUNTY = "County"
    DEFAULT = "Default"
    KEYCHAIN = "Keychain"
    REQUEST_QUEUE = "RequestQueue"
    HOMEOWNER_SEARCH_RESULT = "HomeownerSearchResult"


class BackendObject:

    type = BackendType.DEFAULT

    def __init__(self, uid=None):
        if uid is not None:
            self.uid = uid
        else:
            self.generate_uid()

    def __repr__(self):
        return self.type.__str__() + ": "

    def __str__(self):
        return self.type.__str__() + ": "

    def generate_uid(self):
        self.uid = Backend.get().database().generate_key()

    @staticmethod
    def pyres_to_dictionary(pyres=None, pyre=None):
        dictionary = dict()
        if pyres is not None:
            for item in pyres.pyres:
                dictionary[item.item[0]] = item.item[1]
        elif pyre is not None:
            dictionary = pyre.item[1]

        return dictionary

    def from_dictionary(self, pyres=None, pyre=None):
        dictionary = BackendObject.pyres_to_dictionary(pyres=pyres, pyre=pyre)
        self.uid = dictionary["uid"]
        return dictionary

    def to_dictionary(self):
        return {
            "uid": self.uid
        }
