import pyrebase as pyrebase
from guerillo.config import API


class Backend:

    @staticmethod
    def create_account(user):
        new_account = Backend.get().auth().create_user_with_email_and_password(user.email, user.password)
        user.uid = new_account['localId']  # Store Account UID into User
        Backend.save(user)

    @staticmethod
    def sign_in(user):
        # TODO - Allow User to Sign In With Username & Password or Email & Password
        account = Backend.get().auth().sign_in_with_email_and_password(user.email, user.password)
        user.uid = account['localId']
        return Backend.read(class_name="User", uid=account['localId'])

    @staticmethod
    def get_account_info(id_token):
        Backend.get().auth().get_account_info(id_token)

    @staticmethod
    def save(data):
        if data.__class__.__name__ == "County":
            # Store County, Lock, and Request Queue Data
            Backend.get().database().child("counties").child(data.uid).set(data.to_dictionary())
            Backend.save(data.lock)
            Backend.save(data.request_queue)
        elif data.__class__.__name__ == "Lock":
            # Store County Lock
            Backend.get().database().child("locks").child(data.uid).set(data.to_dictionary())
        elif data.__class__.__name__ == "RequestQueue":
            # Store County Request Queue
            Backend.get().database().child("requests").child(data.uid).set(data.to_dictionary())
        elif data.__class__.__name__ == "User":
            # Store User Data
            Backend.get().database().child("users").child(data.uid).set(data.to_dictionary())
            Backend.save(data.keychain)
        elif data.__class__.__name__ == "Keychain":
            # Store User Keychain
            Backend.get().database().child("keychains").child(data.keychain.uid).set(data.keychain.to_dictionary())

    @staticmethod
    def update(data):
        if data.__class__.__name__ == "County":
            # Update County Data
            Backend.get().database().child("counties").child(data.uid).update(data.to_dictionary())
            Backend.update(data.lock)
            Backend.update(data.request_queue)
        elif data.__class__.__name__ == "Lock":
            # Update County Lock
            Backend.get().database().child("locks").child(data.uid).update(data.to_dictionary())
        elif data.__class__.__name__ == "RequestQueue":
            # Update County Request Queue
            Backend.get().database().child("requests").child(data.uid).update(data.to_dictionary())
        elif data.__class__.__name__ == "User":
            # Update User Data
            Backend.get().database().child("users").child(data.uid).update(data.to_dictionary())
            Backend.update(data.keychain)
        elif data.__class__.__name__ == "Keychain":
            # Update User Keychain
            Backend.get().database().child("keychains").child(data.keychain.uid).update(data.keychain.to_dictionary())

    @staticmethod
    def delete(class_name=None, uid=None):
        if class_name == "County":
            # Remove County, Lock, Request Queue Data + User Keychain References
            return Backend.get().database().child("counties").child(uid).remove()
        elif class_name == "Lock":
            # Remove County Lock
            return Backend.get().database().child("locks").child(uid).remove()
        elif class_name == "RequestQueue":
            # Remove County Request Queue
            return Backend.get().database().child("requests").child(uid).remove()
        elif class_name == "User":
            # Remove User and Keychain Data + User Lock & Request References
            return Backend.get().database().child("users").child(uid).remove()
        elif class_name == "Keychain":
            # Remove User Keychain + User Lock References
            return Backend.get().database().child("keychains").child(uid).remove()

    @staticmethod
    def read(class_name=None, uid=None):
        if class_name == "County":
            # Read County Data
            county_obj = Backend.get().database().child("counties").child(uid).get()
            from guerillo.classes.county import County
            county = County(obj=county_obj,uid="")
            county.lock = Backend.read(class_name="Lock", uid=county_obj["lock_uid"])
            return county
        elif class_name == "Lock":
            # Read County Lock
            lock_obj = Backend.get().database().child("locks").child(uid).get()
            from guerillo.classes.auxiliary_object import AuxiliaryObject, AuxiliaryType
            return AuxiliaryObject(container_uid=lock_obj["county_uid"], aux_type=AuxiliaryType.LOCK, obj=lock_obj)
        elif class_name == "RequestQueue":
            # Read County Request Queue
            request_queue_obj = Backend.get().database().child("locks").child(uid).get()
            from guerillo.classes.auxiliary_object import AuxiliaryObject, AuxiliaryType
            return AuxiliaryObject(container_uid=request_queue_obj["county_uid"], aux_type=AuxiliaryType.REQUEST,
                                   obj=request_queue_obj)
        elif class_name == "User":
            # Read User Data
            user_obj = Backend.get().database().child("users").child(uid).get()
            from guerillo.classes.user import User
            user = User(obj=user_obj)
            user.keychain = Backend.read(class_name="Keychain", uid=user_obj["keychain_uid"])
            return user
        elif class_name == "Keychain":
            # Read User Keychain
            keychain_obj = Backend.get().database().child("keychains").child(uid).get()
            from guerillo.classes.auxiliary_object import AuxiliaryObject, AuxiliaryType
            return AuxiliaryObject(container_uid=keychain_obj["user_uid"], aux_type=AuxiliaryType.KEYCHAIN,
                                   obj=keychain_obj)

    @staticmethod
    def get_configuration():
        return {
            "apiKey": API.KEY,
            "authDomain": API.AUTH_DOMAIN,
            "databaseURL": API.DATABASE_URL,
            "storageBucket": API.STORAGE_BUCKET
        }

    @staticmethod
    def get(): return pyrebase.initialize_app(Backend.get_configuration())
