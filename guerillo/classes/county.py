from cryptography.fernet import Fernet

from guerillo.classes.auxiliary_object import AuxiliaryObject, AuxiliaryType
from guerillo.classes.backend_object import BackendObject


class County(BackendObject):
    def __init__(self, state_fips=None, county_fips=None, key=None, state_name=None, county_name=None,
                 uid=None, lock=None, request_queue=None, obj=None):
        super().__init__(uid=uid)
        self.state_fips = state_fips
        self.state_name = state_name
        self.county_fips = county_fips
        self.county_name = county_name
        if obj is None:
            if key is not None:
                self.key = key
            else:
                self.generate_key()

            if lock is not None:
                self.lock = lock
            else:
                self.lock = AuxiliaryObject(container_uid=self.uid, aux_type=AuxiliaryType.LOCK)

            if request_queue is not None:
                self.request_queue = request_queue
            else:
                self.request_queue = AuxiliaryObject(container_uid=self.uid, aux_type=AuxiliaryType.REQUEST)
        else:
            self.from_dictionary(obj=obj)

    def generate_key(self):
        self.key = Fernet.generate_key()

    def generate_lock(self):
        self.lock = AuxiliaryObject(container_uid=self.uid, aux_type=AuxiliaryType.LOCK)

    def encode_to_user(self, user_uid):
        return Fernet(self.key).encrypt((self.uid + user_uid).encode("utf-8"))

    def decode(self, user_id):
        return Fernet(self.key).decrypt(self.encode_to_user(user_id))

    def get_full_fips_code(self):
        return self.state_fips + self.county_fips

    def get_state_and_county(self):
        return self.county_name + ", " + self.state_name

    def from_dictionary(self, obj=None):
        super().from_dictionary(obj=obj)
        self.state_name = obj["state_name"]
        self.state_fips = obj["state_fips"]
        self.county_name = obj["county_name"]
        self.county_fips = obj["county_fips"]
        self.key = obj["key"].encode("utf-8")


    def to_dictionary(self):
        return {
            ** super().to_dictionary(),
            ** {
                "lock_uid": self.lock.uid,
                "state_name": self.state_name,
                "state_fips": self.state_fips,
                "key": self.key.decode("utf-8"),
                "county_name": self.county_name,
                "county_fips": self.county_fips,
                "request_queue_uid": self.request_queue.uid
            }
        }
