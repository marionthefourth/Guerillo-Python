from .config import General


class Type:
    FILES = "files"
    TEST_MENU = "test_menu"
    DELETE_IDS = "delete_ids"
    START_GUERILLO = "start_guerillo"
    DELETE_TERMS = "delete_terms"
    START_SEARCH = "start_search"
    RESTART_GUERILLO = "restart_guerillo"
    RESTART_SEARCH = "restart_search"
    MANIPULATE_IDS = "manipulate_ids"
    SELECT_SEARCH_TERMS = "select_search_terms"
    MANIPULATE_TERMS = "manipulate_search_terms"
    SAVE_DUPLICATE_RESULTS = "save_duplicate_results"


class Function:
    DISPLAY = 1
    CYCLE_INPUT = 2
    PROCESS_INPUT = 3


class SubRoutines:
    GET_INPUT = 0x0154
    SUBSET_DATA_FROM_INPUT = 0x0156


class Input:
    NEGATIVES = ["n", "no", "nah", "no thank-you", "nope", "na", "no thanks"]
    AFFIRMATIVES = ["y", "yes", "yeah", "sure", "fine", "why not", "let's do it", "k", "okay", "yup", "yea", "yep"]
    ACCEPTABLE_ALL = AFFIRMATIVES + NEGATIVES


class Display:
    ALL = "All URLs:"
    FEED = "Feed URLs:"
    USER = "User URLs:"
    OTHER = "Other URLs:"
    CHANNEL = "Channel URLs:"
    FILTER_AND_SORT = "Filter & Sort URLs:"
    RELATED_REGULAR = "Related URLs [Regular]:"
    RELATED_PLAYLIST = "Related URLs [Playlist]:"
    VALUE_SKIPPED = "[Value Skipped]"
    SUCCESS_WROTE_FILE = "Successfully wrote the file: "
    CONTAINS_RESULTS = "It contains these results: "
    TOTAL_RESULTS_PULLED = "Total Results Pulled: "
    WELCOME_WITH_OPTIONS = "Hello! Welcome! Here are your options: "


class Header:
    INDV_URLS = "--- Individual Urls ---"
    FILE_WRITTEN = "--- File Written ---"
    PARSED_INPUT = "--- Parsed Input ---"
    AVAILABLE_FILES = "--- Available Files ---"
    FINAL_RESULT_URL = "--- Final Result Url ---"
    AVAILABLE_OPTIONS = "--- Available Options ---"
    COUNTDOWN_SECTION = "--- Countdown Section ---"
    SEARCH_RESULT_HTML = "--- Search Result HTML ---"
    TOTAL_NUM_RESULTS = "--- Total Number of Results ---"
    AVAILABLE_SEARCH_TERMS = "--- Available Search Terms ---"


class Option:
    QUIT = "Quit"
    DELETE = "Delete"
    GO_BACK = "Go Back"
    RETURN_TO_MAIN_MENU = "Return to Main Menu"
    DOWNLOAD_CSVS_FROM_DATA = "Download CSVs from Data"
    PULL_CSVS_FROM_TERMS = "Download CSVs From Search Terms"
    PULL_CSVS_FROM_TERM = "Download CSVs From Search Term"


class Request:
    MAX_CAPACITY = "Input the number of results you want:"
    NEW_SEARCH = "Do you want to begin a new search?"
    NEW_OPTION = "Do you want to do anything else?"
    SELECT_OPTION = "Select an appropriate option:"
    SELECT_TERMS = "Which search term or terms do you want?"
    SELECT_IDS = "Which ID or IDs do you want?"
    MANIPULATE_TERMS = "What do you want to do with these search terms?"
    MANIPULATE_TERM = "What do you want to do with this search term?"
    DELETE_TERM = "Are you sure you want to delete this search term?"
    DELETE_TERMS = "Are you sure you want to delete these search terms?"
    ADD_DUPLICATE_IDS = "Some of these item ids are already in your catalog, do you want to add them anyways?"
    NUM_IDS_TO_DOWNLOAD = "Select the number of ids that you want to download:"


class Response:
    FINE = "Okay no problem."
    DELETED_TERM = "I deleted the search term for you!"
    DELETED_TERMS = "I deleted the search terms for you!"
    DELETED_ID = "I deleted the search id for you!"
    DELETED_IDS = "I deleted the search ids for you!"
    RESTART = "Well let's get back to it!"
    FINISHED = "No problem, hope I was able to help :D"
    RESTART_SEARCH = "Well let's see what we can find!"
    ERROR_MISUNDERSTAND = "I didn't quite understand your response..."


def generalize_input(user_input):
    return General.NO if user_input in Input.NEGATIVES else General.YES