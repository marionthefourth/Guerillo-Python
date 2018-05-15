from guerillo.utils.driver_utils.actions.action import Action, ActionType


class ActionGet(Action):

    def __init__(self, type=ActionType.GET, operation=None, operations=None, target=None, value=None):
        super().__init__(type, operation, operations, target, value)

    def single_operation(self, driver=None):
        if self.type == ActionType.GET:
            driver.get(self.operation.get())
