from enum import Enum
from guerillo.classes.backend_object import BackendObject


class AuxiliaryType(Enum):
    LOCK = "county"
    KEYCHAIN = "user"
    REQUEST = "county"


class AuxiliaryObject(BackendObject):

    def __init__(self, uid=None, connected_uid_list=None, container_uid=None, aux_type=None, obj=None):
        super().__init__(uid)
        self.aux_type = aux_type
        self.container_uid = container_uid

        if obj is None:
            self.connected_uid_list = connected_uid_list
        else:
            self.from_dictionary(obj=obj)

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

    def from_dictionary(self, obj=None):
        super().from_dictionary(obj=obj)
        self.connected_uid_list = list()
        for key in obj:
            if self.aux_type+"_uid_" in key:
                self.connected_uid_list.append(obj[key])

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
