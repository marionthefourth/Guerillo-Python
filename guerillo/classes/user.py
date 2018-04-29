from guerillo.classes.auxiliary_object import AuxiliaryObject, AuxiliaryType
from guerillo.classes.backend_object import BackendObject


class User(BackendObject):

    def __init__(self, email=None, username=None, password=None, full_name=None, uid=None, keychain=None, obj=None):
        super().__init__(uid=uid)
        if obj is None:
            self.email = email
            self.username = username
            self.password = password
            self.full_name = full_name
            if keychain is not None:
                self.keychain = keychain
            else:
                # Create New User Keychain
                self.keychain = AuxiliaryObject(container_uid=self.uid, aux_type=AuxiliaryType.KEYCHAIN)
        else:
            self.from_dictionary(obj)

    def from_dictionary(self, obj=None):
        super().from_dictionary(obj=obj)
        self.email = obj["email"]
        self.username = obj["username"]
        self.password = obj["password"]
        self.full_name = obj["full_name"]

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
