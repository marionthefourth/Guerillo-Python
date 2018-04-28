from guerillo.backend.firebase_backend import FirebaseModule as FBM
from guerillo.user import User
from guerillo.utils.state_and_county_data.census_county_api import CensusCountyAPI

user_marion = User(email="me@marionrucker.com", full_name="Marion Rucker", username="marionthefourth")

FBM.create_account(user_marion)



