import pyrebase as pyrebase
from requests import HTTPError

from guerillo.config import API


class Backend:

    @staticmethod
    def create_new_account(user):
        try:
            new_account = Backend.get().auth().create_user_with_email_and_password(user.email, user.password)
            user.uid = new_account['localId']  # Store Account UID into User
            user.keychain.container_uid = user.uid
            Backend.save(user)
            return user
        except HTTPError:
            return None

    @staticmethod
    def sign_in(user):
        database_user = Backend.get_users(user.email)
        if database_user:
            try:
                account = Backend.get().auth().sign_in_with_email_and_password(database_user.email, user.password)
                from guerillo.classes.backend_objects.backend_object import BackendType
                return Backend.read(b_type=BackendType.USER, uid=account['localId'])
            except HTTPError:
                return None
        return None

    @staticmethod
    def get_account_info(id_token):
        Backend.get().auth().get_account_info(id_token)

    @staticmethod
    def save(data):
        Backend.get().database().child(Backend.get_type_folder(data.b_type)).child(data.uid).set(data.to_dictionary())

        from guerillo.classes.backend_objects.backend_object import BackendType
        if data.b_type == BackendType.COUNTY:
            # Store County Lock, and Request Queue Data
            Backend.save(data.lock)
            Backend.save(data.request_queue)
        elif data.b_type == BackendType.USER:
            # Store User Keychain
            Backend.save(data.keychain)

    @staticmethod
    def data_is_new(data):
        from guerillo.classes.backend_objects.backend_object import BackendType
        if data.b_type.is_result():
            result_objects = Backend.get().database().child(Backend.get_type_folder(data.b_type)).get()

            if data.b_type == BackendType.HOMEOWNER:
                from guerillo.classes.backend_objects.result_items.homeowner import Homeowner
                if result_objects.each():
                    for result_object in result_objects.each():
                        homeowner = Homeowner(pyre=result_object)
                        if data == homeowner:
                            return False, homeowner.uid

        return True, data.uid

    @staticmethod
    def update(data):
        from guerillo.classes.backend_objects.backend_object import BackendType
        db = Backend.get().database().child(Backend.get_type_folder(data.b_type)).child(data.uid)

        if data.b_type.is_auxiliary() or data.b_type == BackendType.RESULT:
            db.set(data.to_dictionary())
        else:
            db.update(data.to_dictionary())

        if data.b_type == BackendType.COUNTY:
            # Update County Lock, and Request Queue Data
            Backend.update(data.lock)
            Backend.update(data.request_queue)
        elif data.b_type == BackendType.USER:
            # Update User Keychain
            Backend.update(data.keychain)

    @staticmethod
    def delete(data):
        Backend.get().database().child(Backend.get_type_folder(data.b_type)).child(data.uid).remove()

        from guerillo.classes.backend_objects.backend_object import BackendType
        if data.b_type == BackendType.COUNTY:
            # Delete County Lock and Request Queue Data
            Backend.delete(data.lock)
            Backend.delete(data.request_queue)
            # Remove User Keychain References
            for connected_user in data.lock.get_connected_items():
                connected_user.dequest(data)
                connected_user.keychain.disconnect(data)
                Backend.update(connected_user)
        elif data.b_type == BackendType.USER:
            # Delete User Keychain
            Backend.delete(data.keychain)
            # Remove User Lock and Request References
            for connected_county in data.keychain.get_connected_items():
                connected_county.lock.disconnect(data)
                connected_county.request_queue.diconnect(data)
                Backend.update(connected_county)
        elif data.b_type == BackendType.QUERY:
            # Delete Search Result
            Backend.delete(Backend.read(BackendType.RESULT, data.result_uid))
        elif data.b_type == BackendType.RESULT:
            # Delete Search Query
            Backend.delete(Backend.read(BackendType.QUERY, data.query_uid))
        elif data.b_type == BackendType.RESULT_ITEM:
            # Delete Result Reference in SearchResult
            search_result_objects = Backend.get().database().child(Backend.get_type_folder(BackendType.RESULT)).get()
            for search_result_obj in search_result_objects.each():
                from guerillo.classes.backend_objects.searches.result import Result
                search_result = Result(pyre=search_result_obj, uid="")
                before_size = len(search_result.result_item_list)
                search_result.remove(data)
                after_size = len(search_result.result_item_list)
                if before_size > after_size:
                    Backend.update(search_result)

    @staticmethod
    def read(b_type=None, uid=None, full=True):
        try:
            backend_obj = Backend.get().database().child(Backend.get_type_folder(b_type)).child(uid).get()
        except ValueError:
            return None

        from guerillo.classes.backend_objects.backend_object import BackendType
        if b_type == BackendType.COUNTY:
            # Read County Data
            from guerillo.classes.backend_objects.county import County
            county = County(pyres=backend_obj, uid="")
            if full:
                county.lock = Backend.read(b_type=BackendType.LOCK, uid=county.lock.uid)
                county.request_queue = Backend.read(b_type=BackendType.REQUEST_QUEUE, uid=county.request_queue.uid)
            return county
        elif b_type == BackendType.USER:
            # Read User Data
            from guerillo.classes.backend_objects.user import User
            user = User(pyres=backend_obj, uid="")
            if full:
                user.keychain = Backend.read(b_type=BackendType.KEYCHAIN, uid=user.keychain.uid)
            return user
        elif b_type.is_auxiliary():
            # Read User Keychain, County Lock or Request Queue
            from guerillo.classes.backend_objects.auxiliary_object import AuxiliaryObject
            return AuxiliaryObject(b_type=b_type, pyres=backend_obj)
        elif b_type == BackendType.QUERY:
            # Read Search Query
            from guerillo.classes.backend_objects.searches.query import Query
            return Query(pyres=backend_obj)
        elif b_type == BackendType.RESULT:
            # Read Search Result
            from guerillo.classes.backend_objects.searches.query import Query
            from guerillo.classes.backend_objects.searches.result import Result
            search_result = Result(pyres=backend_obj)
            if full:
                # Then Read Search Query for that Result
                search_result.query = Backend.read(BackendType.QUERY, search_result.twin_uid)
                search_result.result_item_list = list()

                # Then Read each Result Item for that Result
                for result_item_uid in search_result.result_item_uid_list:
                    search_result.result_item_list.append(Backend.read(BackendType.HOMEOWNER, result_item_uid))
            return search_result
        elif b_type.is_result():
            # Read Homeowner, Parcel, or Document
            if b_type == BackendType.HOMEOWNER:
                from guerillo.classes.backend_objects.result_items.homeowner import Homeowner
                return Homeowner(pyres=backend_obj)
            else:
                raise RuntimeError("Invalid BackendType: " + b_type)

    @staticmethod
    def get_search_results(uid=None, result_item_uid=None):
        search_results = list()
        from guerillo.classes.backend_objects.backend_object import BackendType
        search_result_objects = Backend.get().database().child(Backend.get_type_folder(BackendType.RESULT)).get()
        for search_result_obj in search_result_objects.each():
            from guerillo.classes.backend_objects.searches.result import Result
            search_result = Result(pyre=search_result_obj, uid='')
            if uid:
                if search_result.uid == uid:
                    return search_result
            if result_item_uid:
                for search_result_item in search_result.result_item_list:
                    if search_result_item.uid == result_item_uid:
                        search_results.append(search_result)
        if uid:
            return None
        else:
            return search_results

    @staticmethod
    def get_search_queries(uid=None, with_results=False, all=True, s_mode=None):
        search_queries = list()
        from guerillo.classes.backend_objects.backend_object import BackendType
        if all and not (uid and all):
            search_query_objects = Backend.get().database().child(Backend.get_type_folder(BackendType.QUERY)).get()
            for search_query_obj in search_query_objects.each():
                from guerillo.classes.backend_objects.searches.query import Query
                search_query = Query(pyre=search_query_obj, uid='')
                if search_query.s_mode == s_mode or not s_mode:
                    if all or uid and not with_results:
                        if uid:
                            if search_query.uid == uid:
                                return search_query
                        else:
                            search_queries.append(search_query)
                    else:
                        search_result = Backend.read(BackendType.RESULT, search_query.twin_uid, False)
                        if search_result:
                            if with_results:
                                search_queries.append(search_query)
                        else:
                            if not with_results:
                                search_queries.append(search_query)

            if uid:
                return None
            else:
                return search_queries
        else:
            search_query = Backend.read(BackendType.QUERY, uid)
            search_result = Backend.read(BackendType.RESULT, search_query.twin_uid, False)
            if search_result.twin_uid:
                if with_results:
                    return search_query
            else:
                if not with_results:
                    return search_query
            return None

    @staticmethod
    def get_users(email_or_username=None):
        users = list()
        from guerillo.classes.backend_objects.backend_object import BackendType
        user_objects = Backend.get().database().child(Backend.get_type_folder(BackendType.USER)).get()

        for user_obj in user_objects.each():
            from guerillo.classes.backend_objects.user import User
            user = User(pyre=user_obj, uid="")
            if email_or_username:
                if user.email == email_or_username or user.username == email_or_username:
                    user.keychain = Backend.read(b_type=BackendType.KEYCHAIN, uid=user.keychain.uid)
                    return user
            else:
                user.keychain = Backend.read(b_type=BackendType.KEYCHAIN, uid=user.keychain.uid)
                users.append(user)
        if email_or_username:
            return None
        else:
            return users

    @staticmethod
    def get_counties(state_name=None, county_name=None):
        counties = list()
        from guerillo.classes.backend_objects.backend_object import BackendType
        counties_by_state = Backend.get().database().child(Backend.get_type_folder(BackendType.COUNTY)).get()

        for county_obj in counties_by_state.each():
            from guerillo.classes.backend_objects.county import County
            county = County(pyre=county_obj, uid="")
            if (county.state_name == state_name or county.county_name == county_name) \
                    or (state_name is None and county_name is None):
                county.lock = Backend.read(b_type=BackendType.LOCK, uid=county.lock.uid)
                county.request_queue = Backend.read(b_type=BackendType.REQUEST_QUEUE, uid=county.request_queue.uid)
                if county_name and county_name == county.county_name:
                    if state_name == county.state_name:
                        return [county]
                elif state_name == county.state_name:
                    counties.append(county)
                elif not state_name and not county_name:
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
    def get():
        return pyrebase.initialize_app(Backend.get_configuration())

    @staticmethod
    def generate_uid():
        return Backend.get().database().generate_key()

    @staticmethod
    def get_type_folder(b_type):
        from guerillo.classes.backend_objects.backend_object import BackendType
        folder = {
            BackendType.USER: "users",
            BackendType.LOCK: "locks",
            BackendType.COUNTY: "counties",
            BackendType.KEYCHAIN: "keychains",
            BackendType.HOMEOWNER: "homeowners",
            BackendType.REQUEST_QUEUE: "requests",

            BackendType.QUERY: "search_queries",
            BackendType.RESULT: "search_results",
        }.get(b_type, None)

        if not folder:
            from guerillo.classes.backend_objects.searches.search import SearchType
            folder = {
                SearchType.HOMEOWNER: "homeowners",
                SearchType.PARCEL: "parcels",
                SearchType.DOCUMENT: "documents"
            }.get(b_type, None)

        return folder
