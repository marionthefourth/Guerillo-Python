from enum import IntEnum


class ActionType(IntEnum):
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
    FIND_TAGS_BY_NAME = 82
    FIND_TAG_NAME = 83
    MATCH_TEXT = 90
    COMPLEX = 100
    REPEAT = 200
    REPEAT_PREP = 210
    RETURN = 300
    RETURN_PREP = 310

    @staticmethod
    def is_get(action):  # Any Get Operations are handled in 0 <= x < 1
        return ActionType.GET <= action < ActionType.WAIT

    @staticmethod
    def is_wait(action):  # Any Wait Operations are handled in 1 <= x < 2
        return ActionType.WAIT <= action < ActionType.SWITCH

    @staticmethod
    def is_switch(action):  # Any Switch Operations are handled in 2 <= x < 3
        return ActionType.SWITCH <= action < ActionType.CLEAR

    @staticmethod
    def is_clear(action):  # Any Clear Operations are handled in 3 <= x < 4
        return ActionType.CLEAR <= action < ActionType.CLICK

    @staticmethod  # Any Click Operations are handled in 4 <= x < 5
    def is_click(action):
        return ActionType.CLICK <= action < ActionType.SEND_KEYS

    @staticmethod
    def is_send_keys(action):  # Any Send Keys Operations are handled in 5 <= x < 6
        return ActionType.SEND_KEYS <= action < ActionType.ACCEPT

    @staticmethod
    def is_multi_valued(action):
        return action > ActionType.SEND_KEYS


class Operation:
    def __init__(self, target=None, value=None, sub_action=None):
        self.target = target
        self.value = value
        self.sub_action = sub_action

    def get(self):
        # Use if has only one value else returns self
        if not self.target and self.value:
            return self.value
        elif not self.value and self.target:
            return self.target
        else:
            return self


class Action:
    def __init__(self, type=None, operation=None, operations=None, target=None, value=None):
        self.type = type
        self.operation = operation
        self.operations = operations

        if target is not None:
            self.operation = Operation(target)

        if value is not None:
            self.operation = Operation(value=value)

    def single_operation(self, driver=None): pass  # Allow SubClass Implementation

    def multiple_operations(self, driver=None): pass  # Allow SubClass Implementation

    def process(self, driver=None):
        if self.operation:
            self.single_operation(driver)
        elif self.operations:
            self.multiple_operations(driver)
        # TODO - Throw Error for improper Action
