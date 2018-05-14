from guerillo.utils.driver_utils.actions.action import Action, ActionType


class ActionSendKeys(Action):

    def __init__(self, a_type=ActionType.SEND_KEYS, operation=None, operations=None, target=None, value=None):
        super().__init__(a_type, operation, operations, target, value)

    def single_operation(self, driver=None):
        if self.a_type == ActionType.SEND_KEYS:
            self.operation.target.send_keys(self.operation.value)
        elif self.a_type == ActionType.SEND_KEYS_BY_TAG:
            driver.find_element_by_tag_name(self.operation.target).send_keys(self.operation.value)
        elif self.a_type == ActionType.SEND_KEYS_BY_ID:
            driver.find_element_by_id(self.operation.target).send_keys(self.operation.value)
        elif self.a_type == ActionType.SEND_KEYS_BY_NAME:
            driver.find_element_by_name(self.operation.target).send_keys(self.operation.value)
