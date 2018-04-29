import pyrebase as pyrebase

from guerillo.config import API


class Backend:

    @staticmethod
    def create_account(user):
        new_account = Backend.get().auth().create_user_with_email_and_password(user.email, user.password)
        user.uid = new_account['localId']  # Store Account UID into User
        Backend.save(user)

    @staticmethod
    def get_account_info(id_token):
        Backend.get().auth().get_account_info(id_token)

    @staticmethod
    def save(data):
        if data.__class__.__name__ == "County":
            # Store County Data
            Backend.get().database()\
                .child("counties").child(data.state_fips).child(data.uid).set(data.to_dictionary())
            # Store County Lock
            Backend.get().database() \
                .child("locks").child(data.state_fips).child(data.lock.uid).set(data.lock.to_dictionary())
            # Store County Request Queue
            Backend.get().database() \
                .child("requests").child(data.state_fips).child(data.request_queue.uid)\
                .set(data.request_queue.to_dictionary())

        if data.__class__.__name__ == "User":
            # Store User Data
            Backend.get().database()\
                .child("users").child(data.uid).set(data.to_dictionary())
            # Store User Keychain
            Backend.get().database() \
                .child("keychains").child(data.keychain.uid).set(data.keychain.to_dictionary())

    @staticmethod
    def update(data):
        if data.__class__.__name__ == "County":
            # Update County Data
            Backend.get().database()\
                .child("counties").child(data.state_fips).child(data.uid).update(data.to_dictionary())
            # Update County Lock
            Backend.get().database() \
                .child("locks").child(data.state_fips).child(data.lock.uid).update(data.lock.to_dictionary())
            # Update County Request Queue
            Backend.get().database() \
                .child("requests").child(data.state_fips).child(data.request_queue.uid)\
                .update(data.request_queue.to_dictionary())

        if data.__class__.__name__ == "User":
            # Store User Data
            Backend.get().database()\
                .child("users").child(data.uid).update(data.to_dictionary())
            # Store User Keychain
            Backend.get().database() \
                .child("keychains").child(data.keychain.uid).update(data.keychain.to_dictionary())

    @staticmethod
    def delete(child):
        Backend.get().database().child(child).remove()

    @staticmethod
    def read(child):
        Backend.get().database().child(child).get()

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
