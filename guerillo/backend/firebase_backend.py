import pyrebase
from guerillo.config import API


class FirebaseModule:

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

