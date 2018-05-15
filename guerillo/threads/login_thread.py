from threading import Thread
from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.search_query import SearchQuery
from guerillo.classes.backend_objects.user import User
from tkinter import messagebox
from guerillo.threads.window_resize_thread import WindowResizeThread
import tkinter.constants as tc


class LoginThread(Thread):

    def __init__(self, gui_object):
        super().__init__()
        self.gui_object = gui_object
        self.user = Backend.sign_in(User(email=gui_object.username_field.get(),password=gui_object.password_field.get()))
        gui_object.user = self.user


    def run(self):
        if self.user:
            self.gui_object.login_screen.grid_remove()
            self.gui_object.search_screen.grid()
            self.gui_object.status_frame.pack(side=tc.BOTTOM, fill=tc.X)
            self.gui_object.signed_in = True
            self.gui_object.create_account_menu()
            self.gui_object.file_menu.entryconfig(0, state=tc.NORMAL)
            self.gui_object.inject_county_dropdown(self.gui_object.entry_grid_frame,1)
            # self.root.geometry("400x400")
            window_thread = WindowResizeThread(self.gui_object.root, 'expand', 400)
            window_thread.run()
        else:
            messagebox.showinfo("Login Failed","Your username/email and/or password was incorrect.")