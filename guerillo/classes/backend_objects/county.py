from cryptography.fernet import Fernet

from guerillo.classes.backend_objects.auxiliary_object import AuxiliaryObject
from guerillo.classes.backend_objects.backend_object import BackendObject, BackendType


class County(BackendObject):

    b_type = BackendType.COUNTY

    def __init__(self, state_fips=None, county_fips=None, key=None, state_name=None, county_name=None,
                 uid=None, lock=None, request_queue=None, pyres=None, pyre=None, message_data=None):
        super().__init__(uid=uid)
        self.state_fips = state_fips
        self.state_name = state_name
        self.county_fips = county_fips
        self.county_name = county_name
        self.lock = AuxiliaryObject(container_uid=self.uid, b_type=BackendType.LOCK)
        self.request_queue = AuxiliaryObject(container_uid=self.uid, b_type=BackendType.REQUEST_QUEUE)

        if pyres is None and pyre is None:
            if key is not None:
                self.key = key
            else:
                self.generate_key()

            if lock is not None:
                self.lock = lock

            if request_queue is not None:
                self.request_queue = request_queue

        else:
            self.from_dictionary(pyres=pyres, pyre=pyre, message_data=message_data)

    def __repr__(self):
        return super().__repr__() + self.get_full_fips_code() + " - " + self.county_name + ", " + self.state_name

    def __str__(self):
        return super().__str__() + self.get_full_fips_code() + " - " + self.county_name + ", " + self.state_name

    def generate_key(self):
        self.key = Fernet.generate_key()

    def generate_lock(self):
        self.lock = AuxiliaryObject(container_uid=self.uid, b_type=BackendType.LOCK)

    def register_to_user(self, user):
        # Add to Lock
        self.lock.connect(user)
        from guerillo.backend.backend import Backend
        Backend.update(self.lock)
        # Add To User's Keychain
        user.keychain.connect(self)
        Backend.update(user.keychain)

    def deregister_from_user(self, user):
        # Remove from Lock
        self.lock.disconnect(user)
        from guerillo.backend.backend import Backend
        Backend.update(self.lock)
        # Remove from User's Keychain
        user.keychain.disconnect(self)
        Backend.update(user.keychain)

    def authenticate_user(self, user):
        return user in self.lock.connected_uids_list

    def encode(self, user):
        return Fernet(self.key).encrypt((self.uid + user.uid).encode("utf-8"))

    def decode(self, user_id):
        return Fernet(self.key).decrypt(self.register_to_user(user_id))

    def get_full_fips_code(self):
        return self.state_fips + self.county_fips

    def get_state_and_county(self):
        return self.county_name + ", " + self.state_name

    def from_dictionary(self, pyres=None, pyre=None, message_data=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre)
        if dictionary:
            self.state_name = dictionary["state_name"]
            self.state_fips = dictionary["state_fips"]
            self.county_name = dictionary["county_name"]
            self.county_fips = dictionary["county_fips"]
            self.key = dictionary["key"].encode("utf-8")
            self.lock.uid = dictionary["lock_uid"]
            self.request_queue.uid = dictionary["request_queue_uid"]
        return dictionary

    def to_dictionary(self):
        return {
            **super().to_dictionary(),
            "lock_uid": self.lock.uid,
            "state_name": self.state_name,
            "state_fips": self.state_fips,
            "key": self.key.decode("utf-8"),
            "county_name": self.county_name,
            "county_fips": self.county_fips,
            "request_queue_uid": self.request_queue.uid
        }
