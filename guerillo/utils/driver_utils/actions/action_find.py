from guerillo.utils.driver_utils.actions.action import Action, ActionType


class ActionFind(Action):

    def __init__(self, a_type=ActionType.FIND, operation=None, operations=None, target=None, value=None,
                 primary_target=None):
        super().__init__(a_type, operation, operations, target, value)

    def single_operation(self, driver=None):
        if self.a_type == ActionType.FIND_TAGS_BY_NAME:
            return driver.find_elements_by_tag_name(self.operation.get())
