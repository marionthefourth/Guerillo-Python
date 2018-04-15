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


class Directories:
    GENERAL = "/general/"


class Queries:
    GENERAL = "/general/"


class URLs:
    HCPAFL = "http://gis.hcpafl.org/propertysearch/#/nav/Basic%20Search"
    PUBREC = "https://pubrec3.hillsclerk.com/oncore/search.aspx"
    PCPAO = "http://www.pcpao.org/query_name.php"


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
    BIN = "/bin"
    EXPORTS = BIN + "/exports/"
    CSVx = EXPORTS + "/csvs/"


class FileExtensions:
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
    A = "a"
    DIV = "div"