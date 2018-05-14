import time

from selenium.common.exceptions import NoSuchElementException

from guerillo.utils.driver_utils.actions.action import Action, ActionType


class ActionWait(Action):

    # the Operands are the ActionTypes to wait for
    # the Operators are the IDs/Names/Class Names to check for

    def __init__(self, a_type=ActionType.WAIT, operation=None, operations=None, target=None, value=None, timeout=8):
        super().__init__(a_type, operation, operations, target, value)
        self.timeout = timeout

    def single_operation(self, driver=None):
        start_time = time.time()

        while True:
            try:
                if self.a_type != ActionType.WAIT_FOR_CLASS_EXCEPTION:
                    if self.a_type == ActionType.WAIT_FOR_ID:
                        driver.find_element_by_id(self.operation.target)
                    elif self.a_type == ActionType.WAIT_FOR_NAME:
                        driver.find_element_by_name(self.operation.target)
                    elif self.a_type == ActionType.WAIT_FOR_CLASS:
                        driver.find_element_by_class_name(self.operation.target)
                else:
                    driver.find_element_by_class_name(self.operation.target)
                break
            except NoSuchElementException:
                if self.timeout:
                    if (time.time() - start_time) >= self.timeout:
                        print("Had to exit - timed out.")
                        driver.quit()
                        quit()
                if self.a_type == ActionType.WAIT_FOR_CLASS_EXCEPTION:
                    return
