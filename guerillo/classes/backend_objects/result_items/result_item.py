from guerillo.classes.backend_objects.backend_object import BackendObject, BackendType


class ResultItem(BackendObject):

    b_type = BackendType.RESULT_ITEM

    def should_remove(self):
        pass
