from enum import Enum

from guerillo.backend.backend import Backend


class BackendType(Enum):
    USER = "User"
    COUNTY = "County"

    SEARCH = "Search"
    QUERY = "Query"
    RESULT = "Result"

    AUX = "Auxiliary"
    LOCK = "Lock"
    KEYCHAIN = "Keychain"
    REQUEST_QUEUE = "RequestQueue"

    RESULT_ITEM = "ResultItem"
    PARCEL = "Parcel"
    DOCUMENT = "Document"
    HOMEOWNER = "Homeowner"

    DEFAULT = "Default"

    def is_auxiliary(self):
        return self == BackendType.AUX or self == BackendType.KEYCHAIN or\
            self == BackendType.REQUEST_QUEUE or self == BackendType.LOCK

    def is_result(self):
        return self == BackendType.RESULT_ITEM or self == BackendType.HOMEOWNER or \
               self == BackendType.PARCEL or self == BackendType.DOCUMENT


class BackendObject:

    b_type = BackendType.DEFAULT

    def __init__(self, uid=None):
        if uid:
            self.uid = uid
        else:
            self.uid = Backend.generate_uid()

    def __repr__(self):
        return self.b_type.__repr__() + ": "

    def __str__(self):
        return self.b_type.__str__() + ": "

    def from_backend(self, pyres, pyre, message_data):
        return pyres or pyre or message_data

    @staticmethod
    def pyres_to_dictionary(pyres=None, pyre=None, message_data=None):
        dictionary = dict()
        if pyres and pyres.pyres:
            for item in pyres.pyres:
                dictionary[item.item[0]] = item.item[1]
        elif pyre:
            dictionary = pyre.item[1]
        elif message_data:
            return message_data
        else:
            raise ValueError

        return dictionary

    def from_dictionary(self, pyres=None, pyre=None, message_data=None):
        dictionary = BackendObject.pyres_to_dictionary(pyres=pyres, pyre=pyre, message_data=message_data)
        if dictionary:
            self.uid = dictionary["uid"]
            return dictionary
        raise ValueError

    def to_dictionary(self):
        return {"uid": self.uid}
