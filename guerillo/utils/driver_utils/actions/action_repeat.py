from guerillo.utils.driver_utils.actions.action import Action, ActionType


class Loop:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class ActionRepeat(Action):

    def __init__(self, operation=None, operations=None, loop=None, loops=None):
        super().__init__(ActionType.REPEAT, operation, operations)
        self.loop = loop
        self.loops = loops

    def is_at_end(self, action_type, loop_count):
        if self.loop:
            return action_type == self.loop.end
        elif self.loops and len(self.loops) >= loop_count:
            if self.loops[loop_count].end == action_type:
                return True

        return False

    def num_loops(self):
        if self.loop:
            return 1
        elif self.loops:
            return len(self.loops)
        else:
            return 0
