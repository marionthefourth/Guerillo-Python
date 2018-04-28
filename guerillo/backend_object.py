from guerillo.backend.firebase_backend import FirebaseModule


class BackendObject:

    def __init__(self, uid=None):
        if uid is not None:
            self.uid = uid
        else:
            self.generate_uid()

    def generate_uid(self):
        self.uid = FirebaseModule.get().database().generate_key()

    def to_dictionary(self):
        return {
            "uid": self.uid
        }

