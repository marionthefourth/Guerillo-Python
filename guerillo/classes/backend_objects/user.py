from guerillo.classes.backend_objects import BackendType, BackendObject
from guerillo.classes.backend_objects.auxiliary_object import AuxiliaryObject


class User(BackendObject):
    b_type = BackendType.USER

    def __init__(self, email=None, username=None, password=None, full_name=None, uid=None, keychain=None,
                 pyres=None, pyre=None):
        super().__init__(uid=uid)
        # Create New User Keychain
        self.keychain = AuxiliaryObject(container_uid=self.uid, b_type=BackendType.KEYCHAIN)

        if pyres is None and pyre is None:
            self.email = email
            self.username = username
            self.password = password
            self.full_name = full_name
            if keychain is not None:
                self.keychain = keychain
        else:
            self.from_dictionary(pyres=pyres, pyre=pyre)

    def __repr__(self):
        return super().__repr__() + self.username

    def __str__(self):
        return super().__repr__() + self.username

    def has_access_to(self, county_uid=None, county_fips=None, state_fips=None, county_name=None, state_name=None):
        for connected_county in self.keychain.get_connected_items():
            if county_uid is not None and county_uid == connected_county.uid:
                return True
            if county_fips is not None and state_fips is not None:
                if state_fips == connected_county.state_fips and county_fips == connected_county.county_fips:
                    return True
            if state_name is not None and state_name == connected_county.state_name:
                if county_name is not None:
                    if state_name == connected_county.state_name and county_name == connected_county.county_name:
                        return True
                else:
                    return True
        return False

    def get_access_dictionary(self):
        connected_items = self.keychain.get_connected_items()
        state_list = list()
        county_list = [[]]
        for item in connected_items:
            if item.state_name not in state_list:
                state_list.append(item.state_name)

            for (i, state) in enumerate(state_list):
                if item.state_name == state and item.county_name not in county_list[i]:
                    county_list[i].append(item.county_name)
                    break

        access_dictionary = dict()
        for (i, state) in enumerate(state_list):
            access_dictionary[state] = county_list[i]

        return access_dictionary

    def request(self, county):
        if county.request_queue.connected_uids_list is None:
            county.request_queue.connected_uids_list = list()

        if self.uid not in county.request_queue.connected_uids_list:
            county.request_queue.connect(self)
            from guerillo.backend.backend import Backend
            Backend.update(county.request_queue)
        else:
            print(str(self) + " failed to request " + county + ". County has already been requested.")

    def dequest(self, county):
        if county.request_queue.connected_uids_list is None:
            county.request_queue.connected_uids_list = list()

        if self.uid in county.request_queue.connected_uids_list:
            county.request_queue.disconnect(self)
            from guerillo.backend.backend import Backend
            Backend.update(county.request_queue)
        else:
            print(str(self) + " failed to dequest " + county + ". County was not requested prior.")

    def from_dictionary(self, pyres=None, pyre=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre)
        if dictionary:
            self.email = dictionary["email"]
            self.username = dictionary["username"]
            self.full_name = dictionary["full_name"]
            self.keychain.uid = dictionary["keychain_uid"]
        return dictionary

    def to_dictionary(self):
        return {
            **super().to_dictionary(),
            **{
                "email": self.email,
                "username": self.username,
                "full_name": self.full_name,
                "keychain_uid": self.keychain.uid
            }
        }
