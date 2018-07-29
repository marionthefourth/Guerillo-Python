# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:57:50 2018

@author: Kenneth

Table of Contents:

"""
import os
import signal
import subprocess
import tkinter as tk
import tkinter.constants as tc
import webbrowser
from datetime import datetime

from PIL import Image, ImageTk

from guerillo.backend.backend import Backend
from guerillo.classes import Scraper
from guerillo.classes.backend_objects.backend_object import BackendType
from guerillo.classes.backend_objects.searches.query import Query
from guerillo.classes.backend_objects.searches.result import Result
from guerillo.classes.backend_objects.searches.search import SearchState, SearchMode
from guerillo.classes.backend_objects.user import User
from guerillo.classes.exceptions.exceptions import TimeoutException
from guerillo.config import Folders, Resources
from guerillo.threads.search_thread import SearchThread
from guerillo.threads.signup_thread import SignupThread
from guerillo.utils.auto_updater import AutoUpdater
from guerillo.utils.file_storage import FileStorage
from guerillo.utils.sanitizer import Sanitizer


class GUI:
    output_list = []
    entry_fields_list = []
    signed_in = False
    search_button_image = None
    search_button_greyscale_image = None
    result_stream = None

    def expand_window(self, width_target, height_target):
        base_speed = 4.0
        window_width = int(self.root.geometry().split("+")[0].split("x")[0])
        window_height = int(self.root.geometry().split("+")[0].split("x")[1])

        width_delta = width_target - window_width
        if int(width_delta) == 0:  # width doesn't need to be changed
            while window_height < height_target:
                self.root.geometry(str(window_width) + "x" + str(window_height + int(base_speed)))
                self.root.update()
                window_height = int(self.root.geometry().split("+")[0].split("x")[1])
            return  # now we're done

        height_delta = height_target - window_height
        if int(height_delta) == 0:  # height doesn't need to be changed
            while window_width < width_target:
                self.root.geometry(str(window_width + int(base_speed)) + "x" + str(window_height))
                self.root.update()
                window_width = int(self.root.geometry().split("+")[0].split("x")[0])
            return  # now we're done

        # return statements used as a 'break'. if we haven't returned yet, both width and height need to be changed
        if width_delta > height_delta:
            delta_ratio = (width_delta / height_delta) * 1.0
            while not (base_speed * delta_ratio).is_integer():
                base_speed = base_speed + 1.0
            base_speed = int(base_speed)
            while window_width < width_target:  # dimension used is arbitrary but just used to keep with the if statement
                self.root.geometry(
                    str(window_width + int(base_speed * delta_ratio)) + "x" + str(window_height + base_speed))
                self.root.update()
                window_width = int(self.root.geometry().split("+")[0].split("x")[0])
                window_height = int(self.root.geometry().split("+")[0].split("x")[1])

        else:
            delta_ratio = (height_delta / width_delta) * 1.0
            while not (base_speed * delta_ratio).is_integer():
                base_speed = base_speed + 1.0
            base_speed = int(base_speed)
            while window_height < height_target:  # dimension used is arbitrary but just used to keep with the if statement
                self.root.geometry(
                    str(window_width + base_speed) + "x" + str(window_height + int(base_speed * delta_ratio)))
                self.root.update()
                window_width = int(self.root.geometry().split("+")[0].split("x")[0])
                window_height = int(self.root.geometry().split("+")[0].split("x")[1])

    def contract_window(self, width_target, height_target):
        base_speed = 4.0
        window_width = int(self.root.geometry().split("+")[0].split("x")[0])
        window_height = int(self.root.geometry().split("+")[0].split("x")[1])

        width_alpha = width_target - window_width
        if int(width_alpha) == 0:
            while window_height > height_target:
                self.root.geometry(str(window_width) + "x" + str(window_height - int(base_speed)))
                self.root.update()
                window_width = int(self.root.geometry().split("+")[0].split("x")[0])
                window_height = int(self.root.geometry().split("+")[0].split("x")[1])
            return

        height_alpha = height_target - window_height
        if int(height_alpha) == 0:
            while window_width > width_target:
                self.root.geometry(str(window_width - int(base_speed)) + "x" + str(window_height))
                self.root.update()
                window_width = int(self.root.geometry().split("+")[0].split("x")[0])
                window_height = int(self.root.geometry().split("+")[0].split("x")[1])
            return
        # return statements used as a 'break'. if we haven't returned yet, then run as follows
        if width_alpha > height_alpha:
            alpha_ratio = (width_alpha / height_alpha) * 1.0
            while not (base_speed * alpha_ratio).is_integer():
                base_speed = base_speed + 1.0
            base_speed = int(base_speed)
            while window_width > width_target:  # dimension used is arbitrary but just used to keep with the if statement
                self.root.geometry(
                    str(window_width - int(base_speed * alpha_ratio)) + "x" + str(window_height - base_speed))
                self.root.update()
                window_width = int(self.root.geometry().split("+")[0].split("x")[0])
                window_height = int(self.root.geometry().split("+")[0].split("x")[1])

        else:
            alpha_ratio = (height_alpha / width_alpha) * 1.0
            while not (base_speed * alpha_ratio).is_integer():
                base_speed = base_speed + 1.0
            base_speed = int(base_speed)
            while window_height > height_target:  # dimension used is arbitrary but just used to keep with the if statement
                self.root.geometry(
                    str(window_width - base_speed) + "x" + str(window_height - int(base_speed * alpha_ratio)))
                self.root.update()
                window_width = int(self.root.geometry().split("+")[0].split("x")[0])
                window_height = int(self.root.geometry().split("+")[0].split("x")[1])

    def activate_search_button(self, event):
        colorize = True
        for field_reference in self.entry_fields_list:
            if field_reference.get() == "":
                colorize = False
                break
        if colorize:
            if not self.search_button_image:
                self.search_button_image = ImageTk.PhotoImage(
                    Image.open(FileStorage.get_image(Resources.SEARCH_BUTTON)))
            self.search_button.configure(image=self.search_button_image)
            self.search_button.config(command=lambda: self.search_button_method(self.entry_fields_list,
                                                                                self.status
                                                                                )
                                      )
        else:
            if not self.search_button_greyscale_image:
                self.search_button_greyscale_image = ImageTk.PhotoImage(
                    Image.open(FileStorage.get_image(Resources.SEARCH_BUTTON_GREYSCALE)))
            self.search_button.configure(image=self.search_button_greyscale_image)
            self.search_button.config(command=lambda: self.do_nothing)

    def enter_login(self, event):
        self.login()

    def enter_search(self, event):
        self.search_button_method(self.entry_fields_list, self.status)

    def login(self):
        self.sign_up_label.bind("<Button-1>", self.show_signup)
        self.login_status_label.configure(text="")
        self.root.update()
        self.user = Backend.sign_in(User(email=self.username_field.get(), password=self.password_field.get()))
        if self.user:
            counties = self.user.keychain.get_connected_items()
            if counties is None:
                self.login_status_label.configure(text="No counties available.\nEmail support@panoramic.email.",
                                                  fg="red")
                self.expand_window(300, 260)
                return
            self.login_status_label.configure(text="Login successful! Loading searches functions.", fg="green")
            self.expand_window(400, 400)
            self.add_county_dropdown(self.entry_grid_frame, 1)
            self.login_screen.grid_remove()
            self.search_screen.grid()
            self.signed_in = True
            self.create_account_menu()
            self.file_menu.entryconfig(0, state=tc.NORMAL)
            self.status_frame.pack(side=tc.BOTTOM, fill=tc.X)
            # self.root.geometry("400x400")
        else:
            self.login_status_label.configure(text="Your login information was incorrect.", fg="red")

    def sign_out(self):
        self.login_status_label.configure(text="")
        self.search_screen.grid_remove()
        self.login_screen.grid()
        self.status_frame.forget()
        self.clear_inputs()
        self.signed_in = False
        self.account_menu.destroy()
        self.top_menu.delete("Account")
        self.file_menu.entryconfig(0, state=tc.DISABLED)
        # self.root.geometry('300x250')
        self.contract_window(300, 250)

    def do_nothing(self):
        print("would have done something")

    def link_to_pano(self, event):
        webbrowser.open_new(r"http://www.panoramic.global")

    def search_button_method(self, passed_fields_list, passed_status_label):
        selected_county = self.variable.get()
        passed_status_label.configure(text="Getting prepped...")
        search_thread = SearchThread(self, passed_fields_list, passed_status_label)
        search_thread.start()

    def retrieve_inputs_and_run(self, fields_list, status_label):
        input_list = []
        for field_reference in fields_list:
            input_list.append(field_reference.get())

        self.query = Query(inputs=input_list, user_uid=self.user.uid)

        if self.query.is_valid():
            self.sanitize_input_fields(self.query)
            self.status_label = status_label
            # Search by user's accessible counties first and if it isn't in the list they are doing something wrong

            for county in self.user.keychain.get_connected_items():
                if county.county_name == self.variable.get():
                    self.query.county_uid_list.append(county.uid)
            if len(self.query.county_uid_list) > 0:
                self.query.start()


                #  signal.signal(signal.SIGALRM, TimeoutException.handle)

                # Now begin watching after the SearchResult by the UID generated within the SearchQuery
                self.result_stream = Backend.get().database() \
                    .child(Backend.get_type_folder(BackendType.RESULT)) \
                    .child(self.query.twin_uid).stream(self.result_stream_handler)
                main_scraper = Scraper.get_county_scraper(
                    self.query,
                    FileStorage.get_full_path(Folders.EXPORTS),
                )

                main_scraper.run()
            else:
                print("Search not valid.")
        else:
            self.status.configure(text=self.query.invalid_message())

    def result_stream_handler(self, message):
        # signal.alarm(30)
        try:
            if message["data"] and not self.query.is_done():
                self.update_status_via_state(Result(message_data=message["data"]))
        except TimeoutException:
            if not self.query.is_done():
                self.query.pause()
        """
        else:
            # signal.alarm(0)
            continue
        """

    def update_status_via_state(self, result):
        if result.s_state == SearchState.NUMBERING_RESULTS:
            self.status_label.configure(text="Processing " + str(result.max_num_results) + " items")
        elif result.s_state == SearchState.SEARCH_BY_BOOKPAGE:
            self.status_label.configure(
                text="Handling item " + str(result.num_results) + " of " +
                     str(result.max_num_results))
        elif result.s_state == SearchState.SEARCH_BY_NAME:
            self.status_label.configure(text="Taking a deeper look at item " + str(result.num_results) + " of " +
                                             str(result.max_num_results))
        elif result.s_state == SearchState.ENTRY_CLEANING:
            pass
        elif result.is_done():
            self.query.change_mode(SearchMode.DONE)
            self.status_label.configure(text="Successfully found " +
                                             str(result.num_results) + " results. Wrapping up.")
            # Now need to create the csv file based on the result
            report_file_name = FileStorage.get_full_path(Folders.REPORTS) + datetime.now().strftime(
                "%Y-%m-%d %H-%M.csv")
            final_result = Backend.read(BackendType.RESULT, result.uid)
            FileStorage.save_data_to_csv(report_file_name, final_result.to_list())
            os.startfile(report_file_name)
            self.status_label.configure(text="Ready to search.")
        elif result.s_mode == SearchMode.START:
            self.status_label.configure(text="Search starting")
            self.status_label.configure(text="Searching...")
            # self.status_label.configure(text="Now processing " + str(len(self.search_result.results_copy)) + " items")
        elif result.s_mode == SearchMode.PAUSE:
            self.status_label.configure(text="Search paused due to issues. Please run it again.")

    def pull_spinner_data(self):
        return Sanitizer.county_name(self.variable.get()) + "FL"

    def sanitize_input_fields(self, search_query):
        self.lower_bound_input.delete(0, tk.END)
        self.lower_bound_input.insert(0, search_query.lower_bound)
        self.upper_bound_input.delete(0, tk.END)
        self.upper_bound_input.insert(0, search_query.upper_bound)
        self.start_date_input.delete(0, tk.END)
        self.start_date_input.insert(0, search_query.start_date)
        self.end_date_input.delete(0, tk.END)
        self.end_date_input.insert(0, search_query.end_date)

    def clear_inputs(self):
        for field_reference in self.entry_fields_list:
            field_reference.delete(0, 'end')
        self.search_button_greyscale_source_image = Image.open(FileStorage.get_image(Resources.SEARCH_BUTTON_GREYSCALE))
        self.search_button_greyscale_image = ImageTk.PhotoImage(self.search_button_greyscale_source_image)
        self.search_button.configure(image=self.search_button_greyscale_image)
        self.search_button.config(command=lambda: self.do_nothing)
        self.status.configure(text="Ready to search.")

    def open_reports_folder(self):
        print('activated')
        subprocess.call("explorer " + self.reports_path, shell=True)

    def create_core_window(self):
        self.root = tk.Tk()
        self.root.title("Guerillo")
        self.root.iconbitmap(FileStorage.get_image(Resources.ICON))
        self.root.geometry('300x250')  # syntax is 'WidthxHeight'
        self.root.resizable(width=False, height=False)
        self.root.config(background="white")

    def create_status_bar(self):
        self.status_frame = tk.Frame(self.root)
        self.status = tk.Label(self.status_frame, text="Ready to search.", bd=1, relief=tc.SUNKEN, anchor=tc.W)
        self.status.pack(side=tc.BOTTOM, fill=tc.X)

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill=tc.BOTH, expand=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def create_search_screen(self):
        self.search_screen = tk.Frame(self.main_frame, bg="white")
        self.search_screen.grid(row=0, column=0, sticky="nsew")

    def create_signup_screen(self):
        # create core ouline - remove to be called later
        self.signup_screen = tk.Frame(self.main_frame, bg="white")
        self.signup_screen.grid(row=0, column=0, sticky="nsew")
        self.signup_screen.grid_remove()

        # inject the elements frame
        self.signup_elements_frame = tk.Frame(self.signup_screen, bg='white')
        self.signup_elements_frame.place(in_=self.signup_screen, anchor='c', relx=.50, rely=.40)

        # labels and fields
        self.signup_full_name_label = tk.Label(self.signup_elements_frame, text="Full name", bg="white",
                                               font=("Constantia", 12))
        self.signup_full_name_label.grid(row=0, column=0)
        self.signup_full_name_entry = tk.Entry(self.signup_elements_frame, width=25)
        self.signup_full_name_entry.grid(row=1, column=0)
        self.signup_full_name_entry.bind("<Return>", self.enter_signup)

        self.signup_username_label = tk.Label(self.signup_elements_frame, text="Username", bg="white",
                                              font=("Constantia", 12))
        self.signup_username_label.grid(row=2, column=0)
        self.signup_username_entry = tk.Entry(self.signup_elements_frame, width=25)
        self.signup_username_entry.grid(row=3, column=0)
        self.signup_username_entry.bind("<Return>", self.enter_signup)

        self.signup_email_label = tk.Label(self.signup_elements_frame, text="Email", bg="white",
                                           font=("Constantia", 12))
        self.signup_email_label.grid(row=4, column=0)
        self.signup_email_entry = tk.Entry(self.signup_elements_frame, width=25)
        self.signup_email_entry.grid(row=5, column=0)
        self.signup_email_entry.bind("<Return>", self.enter_signup)

        self.signup_password_label = tk.Label(self.signup_elements_frame, text="Password", bg="white",
                                              font=("Constantia", 12))
        self.signup_password_label.grid(row=6, column=0)
        self.signup_password_entry = tk.Entry(self.signup_elements_frame, width=25, show="*")
        self.signup_password_entry.grid(row=7, column=0)
        self.signup_password_entry.bind("<Return>", self.enter_signup)

        self.signup_password_check_label = tk.Label(self.signup_elements_frame, text="Re-enter Password", bg="white",
                                                    font=("Constantia", 12))
        self.signup_password_check_label.grid(row=8, column=0)
        self.signup_password_check_entry = tk.Entry(self.signup_elements_frame, width=25, show="*")
        self.signup_password_check_entry.grid(row=9, column=0)
        self.signup_password_check_entry.bind("<Return>", self.enter_signup)

        # signup button
        self.signup_button_source_image = Image.open(FileStorage.get_image(Resources.SIGN_UP_BUTTON))
        self.signup_button_image = ImageTk.PhotoImage(self.signup_button_source_image)
        self.signup_button = tk.Button(self.signup_elements_frame,
                                       bg="white",
                                       borderwidth=0,
                                       highlightthickness=0,
                                       image=self.signup_button_image,
                                       text="     Login     ",
                                       command=lambda: self.sign_up()
                                       )
        self.signup_button.grid(row=10, column=0)

        # cancel text with function
        self.cancel_label = tk.Label(self.signup_elements_frame, text="Cancel", bg='white', cursor="hand2")
        self.cancel_label.grid(row=11, column=0)
        self.cancel_label.bind("<Button-1>", self.hide_signup)

        # signup screen status label
        self.signup_status_label = tk.Label(self.signup_elements_frame, text="", bg="white")
        self.signup_status_label.grid(row=12, column=0)

    def hide_signup(self, event):
        # TODO: clear the signup fields first
        self.clear_signup_inputs()
        self.signup_status_label.configure(text="")
        self.signup_status_label.update()
        self.signup_screen.grid_remove()
        self.login_screen.grid()
        self.contract_window(300, 250)

    def create_login_screen(self):
        self.login_screen = tk.Frame(self.main_frame, bg="white")
        self.login_screen.grid(row=0, column=0, sticky="nsew")

        self.login_elements_frame = tk.Frame(self.login_screen, bg="white")
        self.login_elements_frame.place(in_=self.login_screen, anchor="c", relx=.50, rely=.40)

        # U/N label and field
        self.username_label = tk.Label(self.login_elements_frame, bg="white", text="Email or Username",
                                       font=("Constantia", 12))
        self.username_label.grid(row=0, column=0)
        self.username_field = tk.Entry(self.login_elements_frame, width=22)
        self.username_field.grid(row=1, column=0)
        self.username_field.bind('<Return>', self.enter_login)

        # PW label and field
        self.password_label = tk.Label(self.login_elements_frame, bg="white", text="Password", font=("Constantia", 12))
        self.password_label.grid(row=2, column=0)
        self.password_field = tk.Entry(self.login_elements_frame, width=22, show="*")
        self.password_field.bind('<Return>', self.enter_login)
        self.password_field.grid(row=3, column=0)
        # login button
        self.login_button_source_image = Image.open(FileStorage.get_image(Resources.LOGIN_BUTTON))
        self.login_button_image = ImageTk.PhotoImage(self.login_button_source_image)
        self.login_button = tk.Button(self.login_elements_frame,
                                      borderwidth=0,
                                      highlightthickness=0,
                                      image=self.login_button_image,
                                      text="     Login     ",
                                      command=lambda: self.login())
        self.login_button.grid(row=4, columnspan=2)
        # spacer TODO: get a canvas line in here or something
        # self.spacer_label = tk.Label(self.login_elements_frame,bg="white",text="  ")
        # self.spacer_label.grid(row=,column=0)
        # sign up option TODO: replace with button??
        self.sign_up_label = tk.Label(self.login_elements_frame, bg="white",
                                      text="Don't have an account? Click to sign up", cursor="hand2")
        self.sign_up_label.grid(row=5, column=0)
        self.sign_up_label.bind("<Button-1>", self.show_signup)
        # TODO: give signup functionality

        # login status label
        self.login_status_label = tk.Label(self.login_elements_frame, bg="white", font=("Constantia", 12))
        self.login_status_label.grid(row=6, column=0, pady=5)

    def show_signup(self, event):
        self.login_screen.grid_remove()
        self.signup_screen.grid()
        self.expand_window(325, 400)

    def enter_signup(self, event):
        self.sign_up()

    def sign_up(self):
        self.signup_status_label.configure(text="")
        self.signup_status_label.update()

        if self.signup_full_name_entry.get() == "":
            self.signup_status_label.configure(text="Please input your full name", fg="red")
            self.signup_status_label.update()
            return

        if self.signup_username_entry.get() == "":
            self.signup_status_label.configure(text="Please input a username", fg="red")
            self.signup_status_label.update()
            return

        if self.signup_email_entry.get() == "":
            self.signup_status_label.configure(text="Please input your email", fg="red")
            self.signup_status_label.update()
            return

        # validate password
        if len(self.signup_password_entry.get()) >= 6:
            if self.signup_password_entry.get() == self.signup_password_check_entry.get():
                # TODO: validate email with regex
                # now that we're validated, move to backend signup
                self.signup_button.configure(state=tc.DISABLED)
                new_user = Backend.create_new_account(
                    User(username=self.signup_username_entry.get(),
                         email=self.signup_email_entry.get(),
                         full_name=self.signup_full_name_entry.get(),
                         password=self.signup_password_entry.get()
                         )
                )
                if new_user:
                    self.sign_up_label.unbind("<Button-1>")
                    signup = SignupThread(new_user, self.login_status_label, self.login_button)
                    signup.start()
                    self.hide_signup("filler because event required")
                    self.username_field.delete(0, tc.END)
                    self.password_field.delete(0, tc.END)
                else:
                    self.signup_status_label.configure(text="Invalid email", fg="red")
                    self.signup_status_label.update()
                self.signup_button.configure(state=tc.NORMAL)
            else:  # this is the password validation fail
                self.signup_status_label.configure(text="Both password fields don't match", fg="red")
                self.signup_status_label.update()
        else:  # this is password length fail
            self.signup_status_label.configure(text="Passwords need to be at least 6 characters", fg="red")
            self.signup_status_label.update()

    def clear_signup_inputs(self):
        self.signup_full_name_entry.delete(0, tc.END)
        self.signup_username_entry.delete(0, tc.END)
        self.signup_email_entry.delete(0, tc.END)
        self.signup_password_entry.delete(0, tc.END)
        self.signup_password_check_entry.delete(0, tc.END)

    def check_for_updates(self):
        AutoUpdater.run()

    def create_logo(self):
        self.logo = ImageTk.PhotoImage(Image.open(FileStorage.get_image(Resources.PANORAMIC_LOGO)))
        # get logo embedded at bottom right corner
        logo_label = tk.Label(self.root, image=self.logo, highlightthickness=0, borderwidth=0, cursor="hand2",
                              anchor=tc.E)
        logo_label.image = self.logo
        logo_label.place(rely=1.0, relx=1.0, x=-11, y=-20, anchor=tc.SE)
        logo_label.bind("<Button-1>", self.link_to_pano)

    def create_top_menu(self):
        # create basic menu
        self.top_menu = tk.Menu(self.root)
        self.root.config(menu=self.top_menu)
        # add a file dropdown menu
        self.file_menu = tk.Menu(self.top_menu, tearoff=False)
        self.top_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New Search / Clear Page",
                                   command=lambda: self.clear_inputs())  # TODO: check if we dont need lamba anymore
        self.file_menu.entryconfig(0, state=tc.DISABLED)
        self.file_menu.add_command(label="Check for Updates", command=lambda: self.check_for_updates())
        self.file_menu.add_command(label="Open Reports Folder", command=lambda: self.open_reports_folder())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.root.destroy)

    def create_account_menu(self):
        self.account_menu = tk.Menu(self.top_menu, tearoff=False)
        self.top_menu.add_cascade(label="Account", menu=self.account_menu)
        # self.account_menu.add_command(label="Account Options", command=lambda: self.do_nothing())
        self.account_menu.add_command(label="Sign Out", command=lambda: self.sign_out())

    def create_entry_grid(self):
        # build entry grid frame (grid layout for text entry components and searches button)
        self.entry_grid_frame = tk.Frame(self.search_screen, bg="white")
        self.entry_grid_frame.place(in_=self.search_screen, anchor="c", relx=.50, rely=.45)

    def add_lower_bound_elements(self, grid_target, row_placement):
        self.lower_bound_label = tk.Label(grid_target, bg="white", text="Min Mortgage Amount", font=("Constantia", 12))
        self.lower_bound_label.grid(row=row_placement, column=0, sticky=tc.E, pady=5)
        self.lower_bound_input = tk.Entry(grid_target, width=15, font="Calibri 13")
        self.lower_bound_input.bind("<Key>", self.activate_search_button)
        self.lower_bound_input.grid(row=row_placement, column=1)
        self.entry_fields_list.append(self.lower_bound_input)

    def add_upper_bound_elements(self, grid_target, row_placement):
        self.upper_bound_label = tk.Label(grid_target, bg="white", text="Max Mortgage Amount", font=("Constantia", 12))
        self.upper_bound_label.grid(row=row_placement, column=0, sticky=tc.E, pady=5)
        self.upper_bound_input = tk.Entry(grid_target, width=15, font="Calibri 13")
        self.upper_bound_input.grid(row=row_placement, column=1)
        self.upper_bound_input.bind("<Key>", self.activate_search_button)
        self.entry_fields_list.append(self.upper_bound_input)

    def add_start_date_elements(self, grid_target, row_placement):
        self.start_date_label = tk.Label(grid_target, bg="white", text="Start Date", font=("Constantia", 12))
        self.start_date_label.grid(row=row_placement, column=0, sticky=tc.E, pady=5)
        self.start_date_input = tk.Entry(grid_target, width=15, font="Calibri 13")
        self.start_date_input.grid(row=row_placement, column=1)
        self.start_date_input.bind("<Key>", self.activate_search_button)
        self.entry_fields_list.append(self.start_date_input)

    def add_end_date_elements(self, grid_target, row_placement):
        self.end_date_label = tk.Label(grid_target, bg="white", text="End Date", font=("Constantia", 12))
        self.end_date_label.grid(row=row_placement, column=0, sticky=tc.E, pady=5)
        self.end_date_input = tk.Entry(grid_target, width=15, font="Calibri 13")
        self.end_date_input.grid(row=row_placement, column=1)
        self.end_date_input.bind("<Key>", self.activate_search_button)
        self.end_date_input.bind("<Return>", self.enter_search)
        self.entry_fields_list.append(self.end_date_input)

    def add_search_button(self, grid_target, row_placement):
        self.search_button_greyscale_image = ImageTk.PhotoImage(
            Image.open(FileStorage.get_image(Resources.SEARCH_BUTTON_GREYSCALE)))
        self.search_button = tk.Button(grid_target,
                                       text="Search",
                                       image=self.search_button_greyscale_image,
                                       highlightthickness=0,
                                       borderwidth=0
                                       )
        self.search_button.grid(row=row_placement, column=0, columnspan=2, pady=10)

    def add_county_dropdown(self, grid_target, row_placement):
        self.arrow_image = ImageTk.PhotoImage(Image.open(FileStorage.get_image(Resources.DOWN_ARROW)))
        self.county_dropdown_label = tk.Label(grid_target, bg="white", text="County to Search", font=("Constantia", 12))
        self.county_dropdown_label.grid(row=row_placement, column=0, sticky=tc.E)
        counties = self.user.keychain.get_connected_items()
        # if counties is None:
        #     self.login_status_label.configure(text="No counties available. Email support@panoramic.email.",fg="red")
        #     return
        counties_list = []
        for county in counties:
            counties_list.append(county.county_name)
        self.county_options = counties_list
        self.variable = tk.StringVar("")
        self.variable.set(self.county_options[0])
        self.county_dropdown = tk.OptionMenu(grid_target, self.variable, *self.county_options,
                                             command=self.update_county_label)
        self.county_dropdown.grid(row=row_placement, column=1)
        self.county_dropdown.config(indicatoron=0, image=self.arrow_image, bg="silver", activebackground="silver",
                                    cursor="hand2")
        self.current_county_label = tk.Label(grid_target, bg="silver", text=self.variable.get())
        self.current_county_label.grid(row=row_placement, column=1, sticky="w", padx=8)
        # self.county_dropdown.configure(state="disabled")

    def update_county_label(self, value):
        county_dict = {}
        for i, county_option in enumerate(self.county_options):
            county_dict[self.county_options[i]] = i
        self.variable.set(self.county_options[county_dict[value]])
        self.current_county_label.configure(text=self.variable.get())

    def add_guerillo_header(self, grid_target, row_placement):
        self.guerillo_header = tk.Label(grid_target, bg="white", text="Guerillo", font=("Constantia", 40))
        self.guerillo_header.grid(row=row_placement, column=0, columnspan=2, pady=3)

    def add_search_query_elements(self, grid_target, row_count):
        self.add_search_button(grid_target, row_count - 1)  # has to be first b/c it needs to exist before creating
        # the upcoming textfields
        self.add_guerillo_header(grid_target, row_count - 7)
        # self.add_county_dropdown(grid_target, row_count - 6)
        self.add_lower_bound_elements(grid_target, row_count - 5)
        self.add_upper_bound_elements(grid_target, row_count - 4)
        self.add_start_date_elements(grid_target, row_count - 3)
        self.add_end_date_elements(grid_target, row_count - 2)

    def __init__(self):
        self.user = None

        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.reports_path = self.root_path + "\\bin\\reports\\"
        self.images_path = self.root_path + "\\res\\img\\"

        self.create_core_window()
        self.create_main_frame()
        self.create_search_screen()
        self.create_signup_screen()
        self.create_logo()
        self.create_status_bar()
        self.create_top_menu()
        self.create_entry_grid()
        self.add_search_query_elements(self.entry_grid_frame, 7)
        self.search_screen.grid_remove()
        self.create_login_screen()

        self.root.mainloop()