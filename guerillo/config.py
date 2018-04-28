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
    KEY = "AIzaSyB2RcGVIugMdzzK6JoFbZb3E4WbQGgLjZM"
    AUTH_DOMAIN = "guerillo-panoramic.firebaseapp.com"
    PROJECT_ID = "guerillo-panoramic"
    DATABASE_URL = "https://guerillo-panoramic.firebaseio.com"
    STORAGE_BUCKET = "guerillo-panoramic.appspot.com"
    MESSAGING_SENDER_ID = "161710239376"


class Directories:
    GENERAL = "/general/"


class Queries:
    GENERAL = "/general/"


class URLs:
    PCPAO = "http://www.pcpao.org/query_name.php"
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

    SCRIPTS = "/guerillo"
    BACKEND = SCRIPTS + "/backend"

    UTILS = SCRIPTS + "/utils"
    FILE_STORAGE = UTILS + "/file_storage"
    COUNTY_KEYGEN = UTILS + "/county_keygen"
    DATA_SANITIZERS = UTILS + "/data_sanitizers"
    STATE_AND_COUNTY_DATA = UTILS + "/state_and_county_data"
    STATE_CODIFIER = UTILS + "/state_codifier"

    BIN = "/bin"
    PYTHON = BIN + "/python"
    EXPORTS = BIN + "/exports/"
    ANSI_DATA = BIN + "/ansi_data/"

    CSVx = EXPORTS + "/csvs/"


class KeyFiles:
    NATIONAL_COUNTY = "national_county.txt"

    @staticmethod
    def get():
        return [KeyFiles.NATIONAL_COUNTY]


class FileExtensions:
    TXT = ".txt"
    CSV = ".csv"
    DYNAMIC = ".%(ext)s"


class OperatingSystems:
    LINUX = "linux"
    LINUX2 = "linux2"
    OSX = "darwin"
    WINDOWS = "win32"


class Classes:
    ANY = "Any"
    INT = "Int"
    BOOL = "Bool"
    STRING = "String"
    MULTIPLE = "Multiple"
    COUNTING_NUMBERS = "Counting_Numbers"


class General:
    TITLE = "title"
    PREPARING_TO_DOWNLOAD = "Preparing to download: "
    BACKWARDS_SLASH = "/"
    FORWARDS_SLASH = "\""
    DBL_BACKWARDS_SLASH = "//"
    DBL_FORWARDS_SLASH = "\\"""
    FORMAT = 'format'
    KEY = 'key'
    NO = "no"
    YES = "yes"
    ALL = "all"


class HTML:
    Window = "window"
    RESULTS = "nR"
    NAME = "Text1"
    SP = "&sp="
    HTTP = "http"
    WWW = "www"
    Q = "&q="
    HREF = "href"
    HTML_BUTTON_ID = "id_button_1324123_friend"
    A = "a"
    DIV = "div"