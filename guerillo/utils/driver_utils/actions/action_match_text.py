from guerillo.utils.driver_utils.actions.action import Action, ActionType


class ActionMatchText(Action):

    def __init__(self, type=ActionType.MATCH_TEXT, operation=None, operations=None, target=None, value=None):
        super().__init__(type, operation, operations, target, value)

    def single_operation(self, driver=None):
        pass
