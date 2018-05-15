class Storage:
    TERMS = "terms"
    NUM_RESULTS = "numResults"
    LINKS_REFERENCE_INDEX = "linkIndex"
    LINKS_INTERNAL_REFERENCE_INDEX = "linkInternalIndex"
    UID = "uid"

    DATE = "date"
    TIME = "time"
    FILE_NAME = "filename"
    FILE_TYPE = "filetype"
    INDEX = "index"


class API:
    PROJECT_ID = "guerillo-panoramic"
    MESSAGING_SENDER_ID = "161710239376"
    KEY = "AIzaSyB2RcGVIugMdzzK6JoFbZb3E4WbQGgLjZM"
    STORAGE_BUCKET = "guerillo-panoramic.appspot.com"
    AUTH_DOMAIN = "guerillo-panoramic.firebaseapp.com"
    DATABASE_URL = "https://guerillo-panoramic.firebaseio.com"


class Directories:
    GENERAL = "\\general\\"


class Queries:
    GENERAL = "\\general\\"


class URLs:
    class PCPAO:
        HOME = "http://www.pcpao.org/"
        QUERY_NAME = HOME + "query_name.php"
        TEXT_1 = QUERY_NAME + "?Text1="
        SEARCH_BY_OR = HOME + "clik.html?pg=" + HOME + "searchbyOR.php"

    class MyPinellasClerk:
        SEARCH_TYPE_CONSIDERATION = 'https://officialrecords.mypinellasclerk.org/search/SearchTypeConsideration'

    PUBREC = "https://pubrec3.hillsclerk.com/oncore/search.aspx"
    HCPAFL = "http://gis.hcpafl.org/propertysearch/#/nav/Basic%20Search"
    CENSUS_COUNTY_CODES = "https://www.census.gov/geo/reference/codes/cousub.html"


class Parsers:
    LXML = "lxml"
    HTML = "html.parser"


class Scripts:
    GET_SCROLL_HEIGHT = "return document.body.scrollHeight"
    SCROLL_TO_BOTTOM = "window.scrollTo(0, document.body.scrollHeight);"


class FileHeaders:
    LINKS_RESULT = "LINKS"


class Folders:
    SCRIPTS = "\\guerillo"
    BACKEND = SCRIPTS + "\\backend"

    UTILS = SCRIPTS + "\\utils"
    FILE_STORAGE = UTILS + "\\file_storage"
    COUNTY_KEYGEN = UTILS + "\\county_keygen"
    DATA_SANITIZERS = UTILS + "\\data_sanitizers"
    STATE_AND_COUNTY_DATA = UTILS + "\\state_and_county_data"
    STATE_CODIFIER = UTILS + "\\state_codifier"

    BIN = "\\bin"
    PYTHON = BIN + "\\python"
    EXPORTS = BIN + "\\exports\\"
    REPORTS = BIN + "\\reports\\"
    ANSI_DATA = BIN + "\\ansi_data\\"
    WEB_DRIVERS = BIN + "\\web_drivers\\"

    CSVx = EXPORTS + "\\csvs\\"


class KeyFiles:
    NATIONAL_COUNTY = "national_county.txt"
    WEBDRIVER = "chromedriver.exe"
    SEARCH_RESULTS = "SearchResults.csv"

    @staticmethod
    def get():
        return [KeyFiles.NATIONAL_COUNTY]


class FileExtensions:
    TXT = ".txt"
    CSV = ".csv"
    DYNAMIC = ".%(ext)s"


class OperatingSystems:
    OSX = "darwin"
    LINUX = "linux"
    LINUX2 = "linux2"
    WINDOWS = "win32"


class Classes:
    ANY = "Any"
    INT = "Int"
    BOOL = "Bool"
    STRING = "String"
    MULTIPLE = "Multiple"
    COUNTING_NUMBERS = "Counting_Numbers"


class General:
    class PCPAO:
        BUTTON_SEARCH = "btnSearch"
        BUTTON_CSV = "btnCsvButton"
        BUTTON = "btnButton"
        RECORD_FROM = "RecordDateFrom"
        RECORD_TO = "RecordDateTo"
        LOWER_BOUND = "LowerBound"
        UPPER_BOUND = "UpperBound"
        BUTTON_SUBMIT = "submitButtonName"
        ITB = "ITB"
        ADDR_NS = "addr_ns"
        TAX_EST = "taxEst"
        NO_RECORDS = "Your search returned no records."

    class WebDriver:
        DEFAULT_DOWNLOAD_DIRECTORY = "download.default_directory"

    TITLE = "title"
    PREPARING_TO_DOWNLOAD = "Preparing to download: "
    BACKWARDS_SLASH = "/"
    FORWARDS_SLASH = "\""
    DBL_BACKWARDS_SLASH = "//"
    DBL_FORWARDS_SLASH = "\\"""
    TEXT_1 = "Text1"
    FORMAT = 'format'
    KEY = 'key'
    NO = "no"
    YES = "yes"
    ALL = "all"
    DEED = "DEED"
    MORTGAGE = "MORTGAGE"
    PREFS = "prefs"
    A = "a"
    BUTTON = "button"
    I_AGREE = "I Agree"
    LINK_BAR = "linkBar"
    VALUE = "value"
    NO_BOOKPAGE = "No Book/Page"
    TOO_MANY_RESULTS = "Too many search results. Skipping this entry."
    DOWNLOADING_ERROR = "Error in downloading data. Please try again. If the problem persists, " \
                        "cry heck and let loose the doggos of war."


class HTML:
    Window = "window"
    RESULTS = "nR"
    NAME = "Text1"
    SP = "&sp="
    TH = "th"
    NUM_RESULTS_1000 = "&nR=1000"
    HTTP = "http"
    WWW = "www"
    Q = "&q="
    TD = "td"
    HREF = "href"
    HTML_BUTTON_ID = "id_button_1324123_friend"
    A = "a"
    DIV = "div"
    TR = "tr"
    T_GRID_CONTENT = "t-grid-content"
    T_NO_DATA = "t-no-data"
    OUTER = "outerHTML"
    PARSER = "html.parser"


class PACKAGES:
    ALL = ['os', 'sys', 'ctypes', 'win32con', 'pyrebase', 'selenium', 'bs4', 'esky', 'time', 'enum', 'csv', 'jedi',
           'tkinter', 'PIL', 'webbrowser', 'cryptography','socks','gcloud']


class SCRIPTS:
    class FOLDERS:
        GUERILLO = "guerillo\\"
        CLASSES = GUERILLO + "classes\\"
        BACKEND_OBJECTS = CLASSES + "backend_objects\\"
        SCRAPERS = CLASSES + "scrapers\\"
        UTILS = GUERILLO + "utils\\"
        STATE_CODIFIER = UTILS + "state_codifier\\"
        BACKEND = GUERILLO + "backend\\"

    # Backend
    BACKEND = FOLDERS.BACKEND + "backend.py"

    BACKENDS_ALL = [BACKEND]
    # Backend Objects
    AUXILARY = FOLDERS.BACKEND_OBJECTS + "auxiliary_object.py"
    BACKEND_OBJECT = FOLDERS.BACKEND_OBJECTS + "backend_object.py"
    COUNTY = FOLDERS.BACKEND_OBJECTS + "county.py"
    HOMEOWNER = FOLDERS.BACKEND_OBJECTS + "homeowner.py"
    HOMEOWNER_SEARCH_RESULT = FOLDERS.BACKEND_OBJECTS + "homeowner_search_result.py"
    SEARCH_QUERY = FOLDERS.BACKEND_OBJECTS + "search_query.py"
    USER = FOLDERS.BACKEND_OBJECTS + "user.py"

    BACKEND_OBJECTS_ALL = [AUXILARY, BACKEND_OBJECT, COUNTY, HOMEOWNER, HOMEOWNER_SEARCH_RESULT, SEARCH_QUERY, USER]
    # Scrapers
    SCRAPER = FOLDERS.SCRAPERS + "scraper.py"
    PINELLAS = FOLDERS.SCRAPERS + "pinellas.py"

    SCRAPERS_ALL = [SCRAPER, PINELLAS]
    # Utils
    SANITIZER = FOLDERS.UTILS + "sanitizer.py"
    DRIVER_UTILS = FOLDERS.UTILS + "driver_utils.py"
    FILE_STORAGE = FOLDERS.UTILS + "file_storage.py"
    CENSUS_COUNTY_API = FOLDERS.UTILS + "census_county_api.py"
    ABBREV_TO_NAME = FOLDERS.STATE_CODIFIER + "abbreviation_to_name.py"
    NAME_TO_ABBREV = FOLDERS.STATE_CODIFIER + "name_to_abbreviation.py"
    STATE_CODIFIER = FOLDERS.STATE_CODIFIER + "state_codifier.py"
    AUTO_UPDATER = FOLDERS.UTILS + "auto_updater.py"

    UTILS_ALL = [SANITIZER, DRIVER_UTILS, FILE_STORAGE, CENSUS_COUNTY_API, ABBREV_TO_NAME, NAME_TO_ABBREV,
                 STATE_CODIFIER, AUTO_UPDATER]
    # General Files
    MAIN = FOLDERS.GUERILLO + "__main__.py"
    TESTS = FOLDERS.GUERILLO + "__tests__.py"
    CONFIG = FOLDERS.GUERILLO + "config.py"
    GUI = FOLDERS.GUERILLO + "gui.py"
    MENU = FOLDERS.GUERILLO + "menu.py"

    GENERAL_ALL = [MAIN, TESTS, CONFIG, GUI, MENU]

    ALL = BACKENDS_ALL + BACKEND_OBJECTS_ALL + UTILS_ALL + GENERAL_ALL

class RESOURCES:
    class Folders:
        RES = "res\\"
        IMG = RES+"img\\"

    DOWNARROW = Folders.IMG+"down_arrow.png"
    LOGINBUTTON = Folders.IMG+"login_button.png"
    PANO = Folders.IMG+"pano.png"
    ICON = Folders.IMG+"phone.ico"
    SEARCHBUTTON = Folders.IMG+"search_button.png"
    SBGREYSCALE = Folders.IMG+"search_button_greyscale.png"
    SIGNUPBUTTON = Folders.IMG+"signup_button.png"

    ALL = [
        DOWNARROW,
        LOGINBUTTON,
        PANO,
        ICON,
        SEARCHBUTTON,
        SBGREYSCALE,
        SIGNUPBUTTON
    ]


