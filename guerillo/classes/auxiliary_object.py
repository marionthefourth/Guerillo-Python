from guerillo.classes.backend_object import BackendObject, BackendType


class AuxiliaryObject(BackendObject):

    type = BackendType.AUX

    def __init__(self, uid=None, connected_uid_list=None, container_uid=None, type=None, pyres=None, pyre=None):
        super().__init__(uid)
        self.type = type
        self.container_uid = container_uid

        if pyres is None and pyre is None:
            self.connected_uid_list = connected_uid_list
        else:
            self.from_dictionary(pyres=pyres, pyre=pyre)

    def get_connected_uid_dictionary(self):
        connected_uid_dict = dict()
        for (i, item) in enumerate(self.connected_uid_list):
            connected_uid_dict[self.get_connected_uid_key(index=i)] = item
        return connected_uid_dict

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
        if self.connected_uid_list is None:
            self.connected_uid_list = list()
            self.connected_uid_list.append(item.uid)
            return

        if item.uid not in self.connected_uid_list:
            self.connected_uid_list.append(item.uid)

    def disconnect(self, item):
        if self.connected_uid_list is None:
            self.connected_uid_list = list()
            return

        if item.uid in self.connected_uid_list:
            self.connected_uid_list = [x if x != item.uid else "" for x in self.connected_uid_list]
            # self.connected_uid_list.remove(item.uid)

    def from_dictionary(self, pyres=None, pyre=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre)
        self.connected_uid_list = list()
        for key in dictionary:
            if self.get_connected_uid_key() in key:
                self.connected_uid_list.append(dictionary[key])

        self.container_uid = dictionary[AuxiliaryObject.get_container_key(self.type)]

    def to_dictionary(self):
        if self.connected_uid_list is not None and len(self.connected_uid_list) != 0:
            return {
                **super().to_dictionary(),
                **{AuxiliaryObject.get_container_key(self.type): self.container_uid},
                **self.get_connected_uid_dictionary()
            }
        else:
            return {
                **super().to_dictionary(),
                **{AuxiliaryObject.get_container_key(self.type): self.container_uid},
            }
