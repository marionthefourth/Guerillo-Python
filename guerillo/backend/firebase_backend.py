import pyrebase
from guerillo.config import API


class FirebaseModule:

    @staticmethod
    def create_account(user):
        new_account = FirebaseModule.get().auth().create_user_with_email_and_password(user.email, user.password)
        user.uid = new_account['idToken']
        FirebaseModule.save(user)


    @staticmethod
    def get_account_info(id_token):
        FirebaseModule.get().auth().get_account_info(id_token)

    @staticmethod
    def save(data):
        if data.__class__.__name__ == "FIPS":
            # Store FIPS Data
            FirebaseModule.get().database()\
                .child("fips").child(data.state_code).child(data.uid).set(data.to_dictionary())
            # Store FIPS Lock
            FirebaseModule.get().database() \
                .child("locks").child(data.state_code).child(data.lock.uid).set(data.lock.to_dictionary())

        if data.__class__.__name__ == "User":
            # Store User Data
            FirebaseModule.get().database()\
                .child("users").child(data.uid).set(data.to_dictionary())
            # Store User Keychain
            FirebaseModule.get().database() \
                .child("keychains").child(data.keychain.uid).set(data.keychain.to_dictionary())

        if data.__class__.__name__ == "CountyKeychain":
            FirebaseModule.get().database()\
                .child("keychains").child(data.uid).set(data.to_dictionary())

    @staticmethod
    def update(child, data):
        FirebaseModule.get().database().child(child).update(data)

    @staticmethod
    def delete(child):
        FirebaseModule.get().database().child(child).remove()

    @staticmethod
    def read(child):
        FirebaseModule.get().database().child(child).get()

    @staticmethod
    def get_configuration():
        return {
            "apiKey": API.KEY,
            "authDomain": API.AUTH_DOMAIN,
            "databaseURL": API.DATABASE_URL,
            "storageBucket": API.STORAGE_BUCKET
        }

    @staticmethod
    def get(): return pyrebase.initialize_app(FirebaseModule.get_configuration())

