from guerillo.utils.driver_utils.actions.action import Action, ActionType


class ActionSwitch(Action):

    def __init__(self, a_type=ActionType.SWITCH, operation=None, operations=None, target=None, value=None):
        super().__init__(a_type, operation, operations, target, value)

    def single_operation(self, driver=None):
        if self.a_type == ActionType.SWITCH_TO_FRAME:
            driver.switch_to.frame(driver.find_element_by_name(self.operation.get()))
        elif self.a_type == ActionType.SWITCH_TO_DEFAULT:
            driver.switch_to.default_content()
        elif self.a_type == ActionType.SWITCH_TO_ALERT:
            alert = driver.switch_to.alert
            #if additional_action == ActionType.ACCEPT:
               # alert.accept()