from guerillo.utils.driver_utils.actions.action import Action, ActionType
from guerillo.utils.driver_utils.actions.action_send_keys import ActionSendKeys


class ActionClear(Action):

    def __init__(self, a_type=ActionType.CLEAR, operation=None, operations=None, target=None, value=None):
        super().__init__(a_type, operation, operations, target, value)

    def single_operation(self, driver=None):
        driver.find_element_by_id(self.operation.target).clear()

        if self.a_type == ActionType.CLEAR_THEN_SEND:
            ActionSendKeys(ActionType.SEND_KEYS_BY_ID, self.operation).process(driver)

    def multiple_operations(self, driver=None):
        for operation in self.operations:
            driver.find_element_by_id(operation.target).clear()

            if self.a_type == ActionType.CLEAR_THEN_SEND:
                ActionSendKeys(ActionType.SEND_KEYS_BY_ID, operation).process(driver)
