from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.search_query import SearchQuery
from guerillo.classes.backend_objects.user import User
from guerillo.classes.scrapers.pinellas import Pinellas
from guerillo.config import Folders
from guerillo.utils.file_storage import FileStorage


def user_tests():
    # print(Backend.get_users(email_or_username="me@marionrucker.com"))
    print(Backend.sign_in(User(email="marionthefourth", password="254theFOURTH452")))


def access_tests():
    test_user = User(username="test", password="222222", email="me@test.com", full_name="Test Account")

    test_user = Backend.sign_in(test_user)
    orange_county = Backend.get_counties(county_name="Orange County")
    pinellas_county = Backend.get_counties(county_name="Pinellas County")
    marion_county = Backend.get_counties(county_name="Marion County")
    # Backend.get_counties(county_name="Pinellas County").register_to_user(test_user)

    print("Users that have access to " + orange_county.__str__() + ": ")
    print(orange_county.lock.get_connected_items())
    print("- - - - ")

    print(test_user.__str__() + " has access to: ")
    print(test_user.keychain.get_connected_items())
    print("- - - - ")

    print(test_user.__str__() + " has access to " + orange_county.__str__() + ":")
    print(test_user.has_access_to(state_name="FL", county_name="Orange County"))
    print("- - - - ")

    print(test_user.__str__() + " has access to " + marion_county.__str__() + ":")
    print(test_user.has_access_to(county_uid=marion_county.uid))
    print("- - - - ")

    print(test_user.__str__() + " has access to " + "Florida:")
    print(test_user.has_access_to(state_name="FL"))
    print("- - - - ")

    print(test_user.__str__() + " has access to " + "Maryland:")
    print(test_user.has_access_to(state_name="Maryland"))
    print("- - - - ")

    print("Access Dictionary of " + test_user.__str__() + ":")
    print(test_user.get_access_dictionary())
    print("- - - - ")


def pinellas_tests():
    search_query = SearchQuery(start_date="04/19/2018", end_date="04/20/2018", lower_bound="200000",
                               upper_bound="600000")
    pinellas = Pinellas(search_query, exports_path=FileStorage.get_full_path(Folders.EXPORTS))
    pinellas.run()
