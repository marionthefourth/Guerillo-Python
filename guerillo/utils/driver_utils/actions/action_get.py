from guerillo.utils.driver_utils.actions.action import Action, ActionType


class ActionGet(Action):

    def __init__(self, a_type=ActionType.GET, operation=None, operations=None, target=None, value=None):
        super().__init__(a_type, operation, operations, target, value)

    def single_operation(self, driver=None):
        if self.a_type == ActionType.GET:
            driver.get(self.operation.get())
