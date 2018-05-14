from guerillo.utils.driver_utils.actions.action import Action, ActionType
from guerillo.utils.driver_utils.actions.action_return import Condition


class ActionComplex(Action):

    elements = None
    selected_element = None
    action_repeat = None
    action_return = None
    loop_count = 1

    def __init__(self, actions=None):
        super().__init__(ActionType.COMPLEX, None, None)
        self.actions = actions
        self.prepare()

    """ Drill Down Mode """
    """ Flat Mode """

    def process(self, driver=None):
        if self.actions:
            return self.multiple_operations(driver)

    def multiple_operations(self, driver=None):
        for loop in range(0, 1 if not self.action_repeat else self.action_repeat.num_loops()):
            for action in self.actions:
                if action.a_type == ActionType.FIND_TAGS_BY_NAME:
                    if self.selected_element:
                        self.elements = self.selected_element.find_elements_by_tag_name(action.operation.get())
                    else:
                        self.elements = driver.find_elements_by_tag_name(action.operation.get())
                elif action.a_type == ActionType.FIND_ID:
                    self.selected_element = driver.find_element_by_id(action.operation.get())
                elif action.a_type == ActionType.MATCH_TEXT:
                    match_fail = True
                    for element in self.elements:
                        if element.text == action.operation.get():
                            self.selected_element = element
                            match_fail = False
                            break
                    if match_fail:
                        if self.action_return and self.action_return.contains_condition(Condition.MATCH_FAIL):
                            return self.action_return.process(driver, condition=Condition.MATCH_FAIL)
                elif action.a_type == ActionType.GET_ATTRIBUTE:
                    driver.get(self.selected_element.get_attribute(action.operation.get()))
                elif action.a_type == ActionType.SEND_KEYS:
                    self.selected_element.send_keys(action.operation.value)
                elif action.a_type == ActionType.GET:
                    action.process(driver)

                # Check If The Complex Action should loop
                if self.action_repeat:
                    if self.action_repeat.is_at_end(action.a_type, self.loop_count-1) and not self.is_at_end(action):
                        self.loop_count += 1
                        break
                    elif self.is_at_end(action) and self.action_return:
                        if self.action_return.contains_condition(Condition.REPEAT_COMPLETION):
                            return self.action_return.process(driver, condition=Condition.REPEAT_COMPLETION)
                elif not self.action_return and self.is_at_end(action):
                    return

                if not self.action_return and not self.action_repeat \
                        or self.is_at_end(action) and not self.action_return:
                    return

    def prepare(self):
        for action in self.actions:
            if action.a_type == ActionType.REPEAT:
                self.action_repeat = action
            if action.a_type == ActionType.RETURN:
                self.action_return = action
                if self.action_return.operations:
                    if self.action_return.is_conditional():
                        for operation in self.action_return.operations:
                            pass

    def is_at_end(self, action):
        if self.action_repeat:
            return self.action_repeat.is_at_end(action.a_type, self.loop_count-1) \
                   and self.loop_count == self.action_repeat.num_loops()
        else:
            return True
