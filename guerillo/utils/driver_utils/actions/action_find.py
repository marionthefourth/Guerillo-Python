from guerillo.utils.driver_utils.actions.action import Action, ActionType


class ActionFind(Action):

    def __init__(self, type=ActionType.FIND, operation=None, operations=None, target=None, value=None):
        super().__init__(type, operation, operations, target, value)

    def single_operation(self, driver=None):
        if self.type == ActionType.FIND_TAGS_BY_NAME:
            return driver.find_elements_by_tag_name(self.operation.get())
