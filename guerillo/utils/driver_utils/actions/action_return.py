from enum import Enum

from guerillo.utils.driver_utils.actions.action import Action, ActionType


class Condition(Enum):
    REPEAT_COMPLETION = "REPEAT_COMPLETION"
    MATCH_FAIL = "MATCH_FAIL"

    @staticmethod
    def is_condition(target):
        for condition in Condition.get_all():
            if target == condition.__str__():
                return True

    @staticmethod
    def get_all():
        return [Condition.REPEAT_COMPLETION, Condition.MATCH_FAIL]


class ActionReturn(Action):

    # the Values are the ActionTypes to wait for
    # the Targets are the IDs/Names/Class Names to check for

    def __init__(self, operation=None, operations=None, value=None, condition=None):
        super().__init__(ActionType.RETURN, operation, operations, target=condition, value=value)

    def contains_condition(self, condition):
        if self.operation:
            return self.operation.target == condition
        elif self.operations:
            for operation in self.operations:
                if operation.target == condition:
                    return True
            return False

        return False

    def is_conditional(self):
        if self.operation:
            return Condition.is_condition(self.operation.target)
        elif self.operations:
            for operation in self.operations:
                if Condition.is_condition(operation.target):
                    return True
            return False

        return False

    def process(self, driver=None, condition=None):
        if condition:
            if self.operation:
                if Condition.is_condition(self.operation.target):
                    if condition == self.operation.target:
                        return self.operation.value
                    else:
                        if self.operation and isinstance(self.operation.value, bool):
                            return not self.operation.value
            elif self.operations:
                if self.contains_condition(condition):
                    for operation in self.operations:
                        if condition == operation.target:
                            return operation.value
                        else:
                            if self.operation and isinstance(operation.value, bool):
                                return not operation.value
        else:
            if self.operation:
                return self.single_operation(driver)
            elif self.operations:
                return self.multiple_operations(driver)

    def single_operation(self, driver=None):
        element = driver
        if self.operation.value == ActionType.FIND_ID:
            element = element.find_element_by_id(self.operation.target)
        elif self.operation.value == ActionType.GET_ATTRIBUTE:
            element = element.get_attribute(self.operation.target)
        elif self.operation.value == ActionType.FIND_TAG_NAME:
            element = element.find_element_by_tag_name(self.operation.target)
        elif self.operation.value == ActionType.FIND_TAGS_BY_NAME:
            element = element.find_elements_by_tag_name(self.operation.target)
        return element

    def multiple_operations(self, driver=None):
        element = driver
        for operation in self.operations:
            if operation.sub_action == ActionType.FIND_ID:
                element = element.find_element_by_id(operation.target)
            elif operation.sub_action == ActionType.GET_ATTRIBUTE:
                element = element.get_attribute(operation.target)
            elif operation.value == ActionType.FIND_TAG_NAME:
                element = element.find_element_by_tag_name(operation.target)
            elif operation.sub_action == ActionType.FIND_TAGS_BY_NAME:
                element = element.find_elements_by_tag_name(operation.target)
        return element
