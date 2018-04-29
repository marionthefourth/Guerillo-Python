from enum import Enum
from guerillo.classes.backend_object import BackendObject


class AuxiliaryType(Enum):
    LOCK = "county"
    KEYCHAIN = "user"
    REQUEST = "county"


class AuxiliaryObject(BackendObject):

    def __init__(self, uid=None, connected_uid_list=None, container_uid=None, aux_type=None):
        super().__init__(uid)
        self.aux_type = aux_type
        self.container_uid = container_uid
        self.connected_uid_list = connected_uid_list

    def connected_uid_list_to_dictionary(self):
        connected_uid_dict = None
        for item in self.connected_uid_list:
            connected_uid_dict[self.aux_type+"_uid_"] = item
        return connected_uid_dict

    def aux_type_to_parent_type(self):
        if self.aux_type == AuxiliaryType.KEYCHAIN:
            return "user"
        else:
            return "county"

    def to_dictionary(self):
        if self.connected_uid_list is not None:
            return {
                **super().to_dictionary(),
                **{self.aux_type_to_parent_type()+"_uid": self.container_uid},
                **self.connected_uid_list_to_dictionary()
            }
        else:
            return {
                **super().to_dictionary(),
                **{self.aux_type_to_parent_type()+"_uid": self.container_uid},
            }
