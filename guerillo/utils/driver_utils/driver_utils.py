from guerillo.config import General
from guerillo.utils.driver_utils.actions.action import ActionType
from guerillo.utils.file_storage import FileStorage
from selenium import webdriver


class DriverUtils:
    def __init__(self, driver=None, exports_path=None):
        if not driver:
            self.create_driver(exports_path)
        else:
            self.driver = driver

    def create_driver(self, exports_path):
        chrome_options = webdriver.ChromeOptions()
        prefs = {General.WebDriver.DEFAULT_DOWNLOAD_DIRECTORY: exports_path}
        chrome_options.add_experimental_option(General.PREFS, prefs)
        # chrome_options.add_argument("window-position=-10000,0")
        self.driver = webdriver.Chrome(FileStorage.get_webdriver(), chrome_options=chrome_options)

    def quit(self):
        self.driver.quit()

    def process(self, action=None, actions=None):
        if actions:
            for action in actions:
                if action.a_type == ActionType.RETURN:
                    return action.process(self.driver)
                else:
                    action.process(self.driver)
        elif action:
            if action.a_type == ActionType.RETURN or action.a_type == ActionType.COMPLEX:
                return action.process(self.driver)
            else:
                action.process(self.driver)
