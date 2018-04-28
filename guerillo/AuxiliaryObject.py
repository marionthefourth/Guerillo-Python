from enum import Enum

from guerillo.backend_object import BackendObject


class AuxiliaryType(Enum):
    LOCK = "user"
    REQUEST = "user"
    KEYCHAIN = "fips"


class AuxiliaryObject(BackendObject):

    def __init__(self, uid=None, connected_uid_list=None, parent_uid=None, aux_type=None):
        super().__init__(uid)
        self.aux_type = aux_type
        self.parent_uid = parent_uid.uid
        self.connected_uid_list = connected_uid_list

    def connected_uid_list_to_dictionary(self):
        connected_uid_dict = None
        for item in self.connected_uid_list:
            connected_uid_dict[self.aux_type+"_uid_"] = item
        return connected_uid_dict

    def aux_type_to_parent_type(self):
        if self.aux_type == AuxiliaryType.KEYCHAIN:
            return "fips"
        else:
            return "user"

    def to_dictionary(self):
        if self.connected_uid_list is not None:
            return {
                **super().to_dictionary(),
                **{self.aux_type_to_parent_type()+"_uid": self.parent_uid},
                **self.connected_uid_list_to_dictionary()
            }
        else:
            return {
                **super().to_dictionary(),
                **{self.aux_type_to_parent_type()+"_uid": self.parent_uid},
            }
