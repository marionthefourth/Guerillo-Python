from guerillo.backend.backend import Backend


class BackendObject:

    def __init__(self, uid=None):
        if uid is not None:
            self.uid = uid
        else:
            self.generate_uid()

    def generate_uid(self):
        self.uid = Backend.get().database().generate_key()

    def from_dictionary(self, obj=None):
        self.uid = obj["uid"]

    def to_dictionary(self):
        return {
            "uid": self.uid
        }

