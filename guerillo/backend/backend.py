import pyrebase as pyrebase

from guerillo.config import API


class Backend:

    @staticmethod
    def create_account(user):
        new_account = Backend.get().auth().create_user_with_email_and_password(user.email, user.password)
        user.uid = new_account['localId']  # Store Account UID into User
        user.keychain.container_uid = user.uid
        Backend.save(user)

    @staticmethod
    def sign_in(user):
        # TODO - Allow User to Sign In With Username & Password or Email & Password
        account = Backend.get().auth().sign_in_with_email_and_password(user.email, user.password)
        from guerillo.classes.backend_objects.backend_object import BackendType
        return Backend.read(type=BackendType.USER, uid=account['localId'])

    @staticmethod
    def get_account_info(id_token):
        Backend.get().auth().get_account_info(id_token)

    @staticmethod
    def save(data):
        Backend.get().database().child(Backend.get_type_folder(data.type)).child(data.uid).set(data.to_dictionary())

        from guerillo.classes.backend_objects.backend_object import BackendType
        if data.type == BackendType.COUNTY:
            # Store County Lock, and Request Queue Data
            Backend.save(data.lock)
            Backend.save(data.request_queue)
        elif data.type == BackendType.USER:
            # Store User Keychain
            Backend.save(data.keychain)

    @staticmethod
    def update(data):
        from guerillo.classes.backend_objects.backend_object import BackendType
        db = Backend.get().database().child(Backend.get_type_folder(data.type)).child(data.uid)
        if data.type == BackendType.REQUEST_QUEUE or data.type == BackendType.LOCK or data.type == BackendType.KEYCHAIN:
            db.set(data.to_dictionary())
        else:
            db.update(data.to_dictionary())

        if data.type == BackendType.COUNTY:
            # Update County Lock, and Request Queue Data
            Backend.update(data.lock)
            Backend.update(data.request_queue)
        elif data.type == BackendType.USER:
            # Update User Keychain
            Backend.update(data.keychain)

    @staticmethod
    def delete(data):
        Backend.get().database().child(Backend.get_type_folder(data.type)).child(data.uid).remove()

        from guerillo.classes.backend_objects.backend_object import BackendType
        if data.type == BackendType.COUNTY:
            # Delete County Lock, and Request Queue Data
            Backend.delete(data.lock)
            Backend.delete(data.request_queue)
            # TODO - Remove User Keychain References
        elif data.type == BackendType.USER:
            # Delete User Keychain
            Backend.delete(data.keychain)
            # TODO - Remove User Lock References

    @staticmethod
    def read(type=None, uid=None):
        backend_obj = Backend.get().database().child(Backend.get_type_folder(type)).child(uid).get()
        from guerillo.classes.backend_objects.backend_object import BackendType
        if type == BackendType.COUNTY:
            # Read County Data
            from guerillo.classes.backend_objects.county import County
            county = County(pyres=backend_obj, uid="")
            county.lock = Backend.read(type=BackendType.LOCK, uid=county.lock.uid)
            county.request_queue = Backend.read(type=BackendType.REQUEST_QUEUE, uid=county.request_queue.uid)
            return county
        elif type == BackendType.USER:
            # Read User Data
            from guerillo.classes.backend_objects.user import User
            user = User(pyres=backend_obj)
            user.keychain = Backend.read(type=BackendType.KEYCHAIN, uid=user.keychain.uid)
            return user
        else:
            # Read User Keychain, County Lock or Request Queue
            from guerillo.classes.backend_objects.auxiliary_object import AuxiliaryObject
            return AuxiliaryObject(type=type, pyres=backend_obj)

    @staticmethod
    def get_counties(state_name=None, county_name=None):
        counties = list()
        from guerillo.classes.backend_objects.backend_object import BackendType
        counties_by_state = Backend.get().database().child(Backend.get_type_folder(BackendType.COUNTY)).get()

        for backend_obj in counties_by_state.each():
            from guerillo.classes.backend_objects.county import County
            county = County(pyre=backend_obj, uid="")
            if (county.state_name == state_name or county.county_name == county_name) \
                    or (state_name is None and county_name is None):
                county.lock = Backend.read(type=BackendType.LOCK, uid=county.lock.uid)
                county.request_queue = Backend.read(type=BackendType.REQUEST_QUEUE, uid=county.request_queue.uid)
                if county_name is not None:
                    return county
                counties.append(county)
        return counties

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

    @staticmethod
    def get_type_folder(type):
        from guerillo.classes.backend_objects.backend_object import BackendType
        return {
            BackendType.COUNTY: "counties",
            BackendType.KEYCHAIN: "keychains",
            BackendType.REQUEST_QUEUE: "requests",
            BackendType.USER: "users",
            BackendType.LOCK: "locks"
        }.get(type, None)
