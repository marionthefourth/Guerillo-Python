import tkinter.constants as tc
from threading import Thread

from guerillo.backend.backend import Backend


class SignupThread(Thread):

    def __init__(self, new_user, login_status_label,login_button):
        super().__init__()
        self.new_user = new_user
        self.login_status_label = login_status_label
        self.login_button = login_button

    def run(self):
        self.login_button.configure(state=tc.DISABLED)
        self.login_status_label.configure(
            text="New account registered!\nWe're wrapping up a few items on our end\nThis may take a minute. Please "
                 "wait..",
            fg="green"
        )
        Backend.get_counties(county_name="Pinellas County", state_name="FL").register_to_user(self.new_user)
        self.login_status_label.configure(text="Everything's been finalized.\nYou can now log in.",fg="green")
        self.login_button.configure(state=tc.NORMAL)

