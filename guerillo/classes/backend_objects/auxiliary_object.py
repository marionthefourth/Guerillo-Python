from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.backend_object import BackendObject, BackendType


class AuxiliaryObject(BackendObject):

    b_type = BackendType.AUX
    connected_items_type = BackendType.DEFAULT

    def __init__(self, uid=None, connected_uids_list=None, container_uid=None, type=None, pyres=None, pyre=None):
        super().__init__(uid)
        self.type = type
        self.set_connected_items_type()
        self.container_uid = container_uid

        if pyres is None and pyre is None:
            self.connected_uids_list = connected_uids_list
        else:
            self.from_dictionary(pyres=pyres, pyre=pyre)

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def get_connected_uids_dictionary(self):
        connected_uids_dict = dict()

        index = 0
        for item in self.connected_uids_list:
            if item != "":
                connected_uids_dict[self.get_connected_uid_key(index)] = item
                index += 1
        return connected_uids_dict

    @staticmethod
    def get_container_key(type):
        if type == BackendType.KEYCHAIN:
            return "user_uid"
        else:
            return "county_uid"

    def get_connected_uid_key(self, index=None):
        if self.type == BackendType.KEYCHAIN:
            connected_uid_key = "county"
        else:
            connected_uid_key = "user"

        connected_uid_key += "_uid_"

        if index is not None:
            connected_uid_key += str('{:03d}'.format(index+1))

        return connected_uid_key

    def connect(self, item):
        if self.connected_uids_list is None:
            self.connected_uids_list = list()
            self.connected_uids_list.append(item.uid)
            return

        if item.uid not in self.connected_uids_list:
            self.connected_uids_list.append(item.uid)
        else:
            print("Failed to connect " + item.__str__() + " to " + self.__str__() + ". Item is already connected")

    def disconnect(self, item):
        if self.connected_uids_list is None:
            self.connected_uids_list = list()
            return

        if item.uid in self.connected_uids_list:
            self.connected_uids_list = [x if x != item.uid else "" for x in self.connected_uids_list]
        else:
            print("Failed to disconnect " + item.__str__() + " from " + self.__str__() + ". Item was never connected")

    def set_connected_items_type(self):
        if self.type == BackendType.KEYCHAIN:
            self.connected_items_type = BackendType.COUNTY
        else:
            self.connected_items_type = BackendType.USER

    def get_connected_items(self):
        return [Backend.read(b_type=self.connected_items_type, uid=connected_item_uid)
                for connected_item_uid in self.connected_uids_list]

    def from_dictionary(self, pyres=None, pyre=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre)
        self.connected_uids_list = list()
        for key in dictionary:
            if self.get_connected_uid_key() in key:
                self.connected_uids_list.append(dictionary[key])

        self.container_uid = dictionary[AuxiliaryObject.get_container_key(self.type)]

    def to_dictionary(self):
        if self.connected_uids_list is not None and len(self.connected_uids_list) != 0:
            return {
                **super().to_dictionary(),
                **{AuxiliaryObject.get_container_key(self.type): self.container_uid},
                **self.get_connected_uids_dictionary()
            }
        else:
            return {
                **super().to_dictionary(),
                **{AuxiliaryObject.get_container_key(self.type): self.container_uid},
            }
