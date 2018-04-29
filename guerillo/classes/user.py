from guerillo.classes.auxiliary_object import AuxiliaryObject, AuxiliaryType
from guerillo.classes.backend_object import BackendObject


class User(BackendObject):

    def __init__(self, email=None, username=None, password=None, full_name=None, uid=None, keychain=None):
        super().__init__(uid=uid)
        self.email = email
        self.username = username
        self.password = password
        self.full_name = full_name
        if keychain is not None:
            self.keychain_uid = keychain
        else:
            # Create New User Keychain
            self.keychain = AuxiliaryObject(container_uid=self.uid, aux_type=AuxiliaryType.KEYCHAIN)

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
