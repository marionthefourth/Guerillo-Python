from guerillo.utils.driver_utils.actions.action import Action, ActionType


class ActionClick(Action):

    def __init__(self, operation=None, operations=None, target=None, value=None, primary_target=None):
        super().__init__(ActionType.CLICK, operation, operations, target, value, primary_target)

    def single_operation(self, driver=None):
        driver.find_element_by_id(self.operation.get()).click()
