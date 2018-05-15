import time
from enum import IntEnum

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from guerillo.config import General
from guerillo.utils.file_storage import FileStorage


class Action(IntEnum):
    GET = 10
    GET_ATTRIBUTE = 11
    WAIT = 20
    WAIT_FOR_ID = 21
    WAIT_FOR_NAME = 22
    WAIT_FOR_CLASS = 23
    WAIT_FOR_CLASS_EXCEPTION = 24
    SWITCH = 30
    SWITCH_TO_FRAME = 31
    SWITCH_TO_DEFAULT = 32
    SWITCH_TO_ALERT = 33
    CLEAR = 40
    CLEAR_THEN_SEND = 41
    CLICK = 50
    SEND_KEYS = 60
    SEND_KEYS_BY_ID = 61
    SEND_KEYS_BY_TAG = 62
    SEND_KEYS_BY_NAME = 63
    ACCEPT = 70
    FIND = 80
    FIND_ID = 81
    FIND_TAG_NAME = 82
    FIND_TAGS_BY_NAME = 83
    MATCH_TEXT = 90
    COMPLEX = 100
    REPEAT = 200
    REPEAT_PREP = 210
    RETURN = 300
    RETURN_PREP = 310
    CHECK = 400

    @staticmethod
    def is_get(action):  # Any Get Operations are handled in 0 <= x < 1
        return Action.GET <= action < Action.WAIT

    @staticmethod
    def is_wait(action):  # Any Wait Operations are handled in 1 <= x < 2
        return Action.WAIT <= action < Action.SWITCH

    @staticmethod
    def is_switch(action):  # Any Switch Operations are handled in 2 <= x < 3
        return Action.SWITCH <= action < Action.CLEAR

    @staticmethod
    def is_clear(action):  # Any Clear Operations are handled in 3 <= x < 4
        return Action.CLEAR <= action < Action.CLICK

    @staticmethod  # Any Click Operations are handled in 4 <= x < 5
    def is_click(action):
        return Action.CLICK <= action < Action.SEND_KEYS

    @staticmethod
    def is_send_keys(action):  # Any Send Keys Operations are handled in 5 <= x < 6
        return Action.SEND_KEYS <= action < Action.ACCEPT

    @staticmethod
    def is_multi_valued(action):
        return action > Action.SEND_KEYS


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
        chrome_options.add_argument("window-position=-10000,0")
        self.driver = webdriver.Chrome(FileStorage.get_webdriver(), chrome_options=chrome_options)

    def quit(self):
        self.driver.quit()

    def action_wait(self, dictionary, action):
        timeout = dictionary.get(0, None)
        if timeout is not None:
            start_time = time.time()
        while True:
            try:
                if action != Action.WAIT_FOR_CLASS_EXCEPTION:
                    for key in dictionary:
                        if action == Action.WAIT_FOR_ID:
                            self.driver.find_element_by_id(key)
                        elif action == Action.WAIT_FOR_NAME:
                            self.driver.find_element_by_name(key)
                        elif action == Action.WAIT_FOR_CLASS:
                            self.driver.find_element_by_class_name(key)
                else:
                    for key in dictionary:
                        self.driver.find_element_by_class_name(key)
                break
            except NoSuchElementException:
                if timeout is not None:
                    if (time.time() - start_time) >= timeout:
                        print("Had to exit - timed out.")
                        self.driver.quit()
                        quit()
                if action == Action.WAIT_FOR_CLASS_EXCEPTION:
                    return
                pass

    def action_switch(self, dictionary, action, additional_action=None):
        if action == Action.SWITCH_TO_FRAME:
            self.driver.switch_to.frame(self.driver.find_element_by_name(dictionary))
        elif action == Action.SWITCH_TO_DEFAULT:
            self.driver.switch_to.default_content()
        elif action == Action.SWITCH_TO_ALERT:
            alert = self.driver.switch_to.alert
            if additional_action == Action.ACCEPT:
                alert.accept()

    def action_clear(self, dictionary, action, additional_action):
        pass

    def action_send_keys(self, action, key, value=None):
        if action == Action.SEND_KEYS:
            key.send_keys(value)
        elif action == Action.SEND_KEYS_BY_TAG:
            self.driver.find_element_by_tag_name(key).send_keys(value)
        elif action == Action.SEND_KEYS_BY_ID:
            self.driver.find_element_by_id(key).send_keys(value)
        elif action == Action.SEND_KEYS_BY_NAME:
            self.driver.find_element_by_name(key).send_keys(value)

    def action_multi(self, dictionary):
        for index_key in dictionary:
            action_dictionary = dictionary[index_key]
            for action_key in action_dictionary:
                if isinstance(action_dictionary[action_key], dict):
                    action_items_dictionary = action_dictionary[action_key]
                    if action_key != Action.COMPLEX and action_key != Action.RETURN:
                        for item in action_items_dictionary:
                            value = action_items_dictionary[item]
                            self.handle_action(action_key, item, value=value)
                    elif action_key == Action.COMPLEX:
                        self.action_complex(action_items_dictionary)
                    elif action_key == Action.RETURN:
                        return self.action_return(action_items_dictionary)
                else:
                    action_item = action_dictionary[action_key]
                    self.handle_action(action_key, action_item)

    def handle_action(self, action, key, value=None):
        if action == Action.GET:
            self.driver.get(key)
        elif Action.is_wait(action):
            self.action_wait({key: value}, action)
        elif Action.is_switch(action):
            self.action_switch(key, action)
        elif action == Action.CLEAR:
            self.driver.find_element_by_id(key).clear()
        elif action == Action.CLICK:
            self.driver.find_element_by_id(key).click()
        elif action == Action.CLEAR_THEN_SEND:
            self.handle_action(Action.CLEAR, key)
            self.handle_action(Action.SEND_KEYS_BY_ID, key, value)
        elif Action.is_send_keys(action):
            self.action_send_keys(action, key, value)
        elif action == Action.COMPLEX:
            self.action_complex(action, key, value)
        elif action == Action.RETURN:
            return self.action_return({key: value})

    def action_complex(self, dictionary, elements=None, selected_element=None, return_type=None, return_values=None):
        elements = None
        selected_element = None
        return_type = None
        return_values = []
        action_checks = {}
        repeat_starts = []
        repeat_ends = []
        loop_count = 1
        for sub_action_key in dictionary:
            sub_action_dict = dictionary[sub_action_key]
            if sub_action_key == Action.FIND_TAGS_BY_NAME:
                elements = self.driver.find_elements_by_tag_name(dictionary[sub_action_key])
            elif sub_action_key == Action.FIND_TAG_NAME:
                elements = []
                elements.append(self.driver.find_element_by_tag_name(dictionary[sub_action_key]))
            elif sub_action_key == Action.CHECK:
                for value in return_values:
                    if value == True and len(return_values) == 1:
                        return "Throw an error. Y'done fucked up."
            elif sub_action_key == Action.MATCH_TEXT:
                for element in elements:
                    if element.text == dictionary[sub_action_key]:
                        selected_element = element
                        return_values.append(True)
                        break
                if not return_values and not repeat_ends or loop_count == len(repeat_ends) and not return_values:
                    return
                elif return_values and not repeat_ends or return_values and loop_count == len(repeat_ends):
                    return return_values
            elif sub_action_key == Action.GET_ATTRIBUTE:
                self.driver.get(selected_element.get_attribute(dictionary[sub_action_key]))
            elif sub_action_key == Action.SEND_KEYS:
                selected_element.send_keys(dictionary[sub_action_key])
            elif sub_action_key == Action.RETURN_PREP:
                for return_value in sub_action_dict:
                    return_values.append(return_value)
                    action_check_dict = sub_action_dict[return_value]
                    if isinstance(action_check_dict, dict):
                        for action_check in sub_action_dict[return_value]:
                            action_checks[return_value] = action_check
                    else:
                        for action_check in sub_action_dict:
                            action_checks[return_value] = action_check

            elif sub_action_key == Action.REPEAT_PREP:
                for repeat_index in sub_action_dict:
                    for loop_key in sub_action_dict[repeat_index]:
                        repeat_starts.append(loop_key)
                        repeat_ends.append(sub_action_dict[repeat_index][loop_key])
            elif sub_action_key == Action.RETURN:
                return self.action_return(dictionary[sub_action_key])
            if repeat_ends:
                for repeat_start in repeat_starts:
                    if repeat_start == sub_action_key:
                        pass
                for repeat_end in repeat_ends:
                    if repeat_end == sub_action_key:
                        loop_count += 1
                        return self.action_complex(dictionary, elements, selected_element, return_type, return_values)
            elif repeat_ends and loop_count == len(repeat_ends):
                return

    def action_return(self, dictionary):
        element = self.driver
        for sub_action_key in dictionary:
            if sub_action_key == Action.FIND_ID:
                element = element.find_element_by_id(dictionary[sub_action_key])
            elif sub_action_key == Action.GET_ATTRIBUTE:
                element = element.get_attribute(dictionary[sub_action_key])
            elif sub_action_key == Action.FIND_TAGS_BY_NAME:
                element = element.find_element_by_tag_name(dictionary[sub_action_key])
        return element
