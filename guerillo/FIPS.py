from cryptography.fernet import Fernet

from guerillo.AuxiliaryObject import AuxiliaryObject, AuxiliaryType
from guerillo.backend_object import BackendObject


class FIPS(BackendObject):
    def __init__(self, state_code, county_code, key=None, state_name=None, county_name=None,
                 uid=None, lock=None, request_queue=None):
        super().__init__(uid=uid)
        self.state_code = state_code
        self.state_name = state_name
        self.county_code = county_code
        self.county_name = county_name
        if key is not None:
            self.key = key
        else:
            self.generate_key()

        if lock is not None:
            self.lock = lock
        else:
            self.lock = AuxiliaryObject(parent_uid=self.uid, aux_type=AuxiliaryType.LOCK)

        if request_queue is not None:
            self.request_queue = request_queue
        else:
            self.request_queue = AuxiliaryObject(parent_uid=self.uid, aux_type=AuxiliaryType.REQUEST)

    def generate_key(self):
        self.key = Fernet.generate_key()

    def generate_lock(self):
        self.lock = AuxiliaryObject(parent_uid=self.uid, aux_type=AuxiliaryType.LOCK)

    def encode_to_user(self, user_uid):
        return Fernet(self.key).encrypt((self.uid + user_uid).encode("utf-8"))

    def decode(self, user_id):
        return Fernet(self.key).decrypt(self.encode_to_user(user_id))

    def get_code(self):
        return self.state_code + self.county_code

    def get_state_and_county(self):
        return self.county_name + ", " + self.state_name

    def to_dictionary(self):
        return {
            ** super().to_dictionary(),
            ** {
                "lock_uid": self.lock.uid,
                "state_name": self.state_name,
                "state_code": self.state_code,
                "key": self.key.decode("utf-8"),
                "county_name": self.county_name,
                "county_code": self.county_code
            }
        }
