from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.searches.query import Query
from guerillo.classes.backend_objects.user import User
from guerillo.classes.scrapers.florida.pinellas_fl import PinellasFL
from guerillo.config import Folders
from guerillo.utils.file_storage import FileStorage
from guerillo.classes.backend_objects import county


def user_tests():

    # print(Backend.get_users(email_or_username="me@marionrucker.com"))
    print(Backend.sign_in(User(email="cbettez@xxifinancial.com", password="Colton2018")))


def query_validation_tests():
    lower_bound = "124,0124.80906"
    upper_bound = "$2400021,0"
    start_date = "5\\3-2018"
    end_date = "05/24/2018"

    search_query = Query(start_date, end_date, lower_bound, upper_bound)

    print(search_query)
    print(" - - - ")

    print("Query is valid: " + str(search_query.is_valid()))
    print(search_query.invalid_message())
    print(" - - - ")

    print(search_query)


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

    print(test_user.__str__() + " has access to " + "florida:")
    print(test_user.has_access_to(state_name="FL"))
    print("- - - - ")

    print(test_user.__str__() + " has access to " + "Maryland:")
    print(test_user.has_access_to(state_name="Maryland"))
    print("- - - - ")

    print("Access Dictionary of " + test_user.__str__() + ":")
    print(test_user.get_access_dictionary())
    print("- - - - ")


def pinellas_tests():
    """ to register to user """
    user = Backend.sign_in(User(email=PUTEMAILHERE, password=PUTPASSWORDHERE))
    pinellas_county = Backend.get_counties(county_name="Pinellas County", state_name="FL")
    pinellas_county[0].register_to_user(user)
    """"""
    search_query = Query(start_date="04/19/2018", end_date="04/20/2018", lower_bound="200000",
                         upper_bound="600000")
    pinellas = PinellasFL(search_query, exports_path=FileStorage.get_full_path(Folders.EXPORTS))
    pinellas.run()
