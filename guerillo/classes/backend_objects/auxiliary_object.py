from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.backend_object import BackendObject, BackendType


class AuxiliaryObject(BackendObject):
    b_type = BackendType.AUX
    connected_items_type = BackendType.DEFAULT

    def __init__(self, uid=None, connected_uid_list=None, container_uid=None, b_type=BackendType.AUX,
                 pyres=None, pyre=None):
        super().__init__(uid)
        self.b_type = b_type
        self.set_connected_items_type()
        self.container_uid = container_uid

        if pyres is None and pyre is None:
            self.connected_uid_list = connected_uid_list
        else:
            self.from_dictionary(pyres=pyres, pyre=pyre)

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    @staticmethod
    def get_uid_dictionary_from_uid_list(b_object, uid_list, v_index=0):
        uid_dict = dict()

        index = 0
        if uid_list:
            for item in uid_list:
                if item != "":
                    uid_dict[AuxiliaryObject.get_connected_uid_key(b_object, len(uid_list), index, v_index)] = item
                    index += 1
            return uid_dict
        return None

    @staticmethod
    def get_uid_dictionary_from_list(b_object, item_list, v_index=0):
        uid_dict = dict()

        index = 0
        if item_list:
            for item in item_list:
                if item:
                    uid_dict[AuxiliaryObject.get_connected_uid_key(b_object, index, v_index)] = item.uid
                    index += 1
            return uid_dict
        return None

    @staticmethod
    def get_container_key(b_type):
        if b_type == BackendType.KEYCHAIN:
            return "user_uid"
        else:
            return "county_uid"

    @staticmethod
    def get_connected_uid_key(b_object, list_size=0, index=None, v_index=0):
        if b_object.b_type == BackendType.KEYCHAIN or b_object.b_type == BackendType.RESULT:
            if v_index == 0:
                connected_uid_key = "county"
            else:
                connected_uid_key = "homeowner"
        else:
            connected_uid_key = "user"

        connected_uid_key += "_uid"

        if index is not None:
            connected_uid_key += "_" + AuxiliaryObject.get_dict_index(list_size, index)

        return connected_uid_key

    @staticmethod
    def get_dict_index(list_size, index):
        places = str(len(str(list_size)))
        index_format = '{:0'+places+'d}'
        return str(index_format.format(index + 1))

    def connect(self, item):
        if self.connected_uid_list is None:
            self.connected_uid_list = list()
            self.connected_uid_list.append(item.uid)
            return

        if item.uid not in self.connected_uid_list:
            self.connected_uid_list.append(item.uid)
        else:
            print("Failed to connect " + item.__str__() + " to " + self.__str__() + ". Item is already connected")

    def disconnect(self, item):
        if self.connected_uid_list is None:
            self.connected_uid_list = list()
            return

        if item.uid in self.connected_uid_list:
            self.connected_uid_list = [x if x != item.uid else "" for x in self.connected_uid_list]
        else:
            print("Failed to disconnect " + item.__str__() + " from " + self.__str__() + ". Item was never connected")

    def set_connected_items_type(self):
        if self.b_type == BackendType.KEYCHAIN:
            self.connected_items_type = BackendType.COUNTY
        else:
            self.connected_items_type = BackendType.USER

    def get_connected_items(self):
        try:
            return [Backend.read(b_type=self.connected_items_type, uid=connected_item_uid)
                    for connected_item_uid in self.connected_uid_list]
        except AttributeError:
            return None

    def from_dictionary(self, pyres=None, pyre=None, v_index=0):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre)
        if dictionary:
            self.connected_uid_list = AuxiliaryObject.get_uid_list_from_dictionary(self, dictionary, v_index)
            self.container_uid = dictionary[AuxiliaryObject.get_container_key(self.b_type)]

    @staticmethod
    def get_uid_list_from_dictionary(b_object, dictionary, v_index=0):
        uid_list = list()
        for key in dictionary:
            if AuxiliaryObject.get_connected_uid_key(b_object, v_index=v_index) in key:
                uid_list.append(dictionary[key])
        return uid_list

    def to_dictionary(self):
        main_dict = {
            **super().to_dictionary(),
            **{AuxiliaryObject.get_container_key(self.b_type): self.container_uid},
        }
        if self.connected_uid_list and len(self.connected_uid_list) != 0:
            return {
                **main_dict,
                **AuxiliaryObject.get_uid_dictionary_from_uid_list(self, self.connected_uid_list)
            }
        else:
            return main_dict
