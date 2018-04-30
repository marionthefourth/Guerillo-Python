from guerillo.classes.auxiliary_object import AuxiliaryObject
from guerillo.classes.backend_object import BackendObject, BackendType


class User(BackendObject):

    type = BackendType.USER

    def __init__(self, email=None, username=None, password=None, full_name=None, uid=None, keychain=None,
                 pyres=None, pyre=None):
        super().__init__(uid=uid)
        # Create New User Keychain
        self.keychain = AuxiliaryObject(container_uid=self.uid, type=BackendType.KEYCHAIN)

        if pyres is None and pyre is None:
            self.email = email
            self.username = username
            self.password = password
            self.full_name = full_name
            if keychain is not None:
                self.keychain = keychain

        else:
            self.from_dictionary(pyres=pyres, pyre=pyre)

    def from_dictionary(self, pyres=None, pyre=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre)
        self.email = dictionary["email"]
        self.username = dictionary["username"]
        self.full_name = dictionary["full_name"]
        self.keychain.uid = dictionary["keychain_uid"]

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
