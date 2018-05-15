from threading import Thread


class SearchThread(Thread):

    def __init__(self, gui_object, fields_list, status_label):
        super().__init__()
        self.gui_object = gui_object
        self.status_label = status_label
        self.fields_list = fields_list

    def run(self):
        self.gui_object.retrieve_inputs_and_run(self.fields_list, self.status_label)
