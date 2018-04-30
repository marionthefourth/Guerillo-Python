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

    def generate_uid(self):
        self.uid = Backend.get().database().generate_key()

    @staticmethod
    def pyre_to_dictionary(obj=None):
        dictionary = dict()
        for item in obj.pyres:
            dictionary[item.item[0]] = item.item[1]

        return dictionary

    def from_dictionary(self, obj=None):
        dictionary = BackendObject.pyre_to_dictionary(obj=obj)
        self.uid = dictionary["uid"]
        return dictionary

    def to_dictionary(self):
        return {
            "uid": self.uid
        }
