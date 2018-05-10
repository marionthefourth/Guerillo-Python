# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:57:50 2018

@author: Kenneth

Table of Contents:

"""
import tkinter.constants as tc
import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import os
from threading import Thread
import subprocess
from tkinter import messagebox

from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.search_query import SearchQuery
from guerillo.classes.backend_objects.user import User
from guerillo.classes.scrapers.pinellas import Pinellas
from guerillo.config import Folders
from guerillo.threads.search_thread import SearchThread
from guerillo.threads.window_resize_thread import WindowResizeThread
from guerillo.utils.file_storage import FileStorage
from guerillo.threads.login_thread import LoginThread


class GUI:
    output_list = []
    entry_fields_list = []
    signed_in = False
    search_button_image = None
    search_button_greyscale_image = None

    def expand_window(self,size):
        self.window_width = int(self.root.geometry().split("+")[0].split("x")[0])
        self.window_height = int(self.root.geometry().split("+")[0].split("x")[1])
        while self.window_width < size:
            self.root.geometry(str(self.window_width + 6) + "x" + str(self.window_height + 10))
            self.root.update()
            self.window_width = int(self.root.geometry().split("+")[0].split("x")[0])
            self.window_height = int(self.root.geometry().split("+")[0].split("x")[1])

    def contract_window(self,size):
        self.window_width = int(self.root.geometry().split("+")[0].split("x")[0])
        self.window_height = int(self.root.geometry().split("+")[0].split("x")[1])
        while self.window_width > size:
            self.root.geometry(str(self.window_width - 6) + "x" + str(self.window_height - 10))
            self.root.update()
            self.window_width = int(self.root.geometry().split("+")[0].split("x")[0])
            self.window_height = int(self.root.geometry().split("+")[0].split("x")[1])

    def activate_search_button(self, event):
        colorize = True
        for field_reference in self.entry_fields_list:
            if field_reference.get() == "":
                colorize = False
                break
        if colorize:
            if not self.search_button_image:
                self.search_button_image = ImageTk.PhotoImage(Image.open(self.images_path + "search_button.png"))
            self.search_button.configure(image=self.search_button_image)
            self.search_button.config(command=lambda: self.search_button_method(self.entry_fields_list,
                                                                                self.status
                                                                                )
                                      )
        else:
            if not self.search_button_greyscale_image:
                self.search_button_greyscale_image = ImageTk.PhotoImage(
                    Image.open(self.images_path + "search_button_greyscale.png"))
            self.search_button.configure(image=self.search_button_greyscale_image)
            self.search_button.config(command=lambda: self.do_nothing)

    def enter_login(self,event):
        self.login()

    def enter_search(self,event):
        self.search_button_method(self.entry_fields_list,self.status)

    def login(self):
        self.login_status_label.configure(text="")
        self.root.update()
        self.user = Backend.sign_in(User(email=self.username_field.get(),password=self.password_field.get()))
        if self.user:
            self.login_status_label.configure(text="Login successful! Loading search functions.",fg="green")
            self.expand_window(400)
            self.inject_county_dropdown(self.entry_grid_frame, 1)
            self.login_screen.grid_remove()
            self.search_screen.grid()
            self.signed_in = True
            self.create_account_menu()
            self.file_menu.entryconfig(0, state=tc.NORMAL)
            self.status_frame.pack(side=tc.BOTTOM, fill=tc.X)
            # self.root.geometry("400x400")
        else:
            self.login_status_label.configure(text="Your login information was incorrect.",fg="red")

    def sign_out(self):
        self.login_status_label.configure(text="")
        self.search_screen.grid_remove()
        self.login_screen.grid()
        self.status_frame.forget()
        self.clear_inputs(self.entry_fields_list)
        self.signed_in = False
        self.account_menu.destroy()
        self.top_menu.delete("Account")
        self.file_menu.entryconfig(0, state=tc.DISABLED)
        # self.root.geometry('300x250')
        self.contract_window(300)

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
        pinellas_instance = Pinellas(
            #search_query=SearchQuery(inputs=input_list),
            search_query=SearchQuery(lower_bound="250000",upper_bound="300000",start_date="05/01/2018",end_date="05/02/2018"),
            exports_path=FileStorage.get_full_path(Folders.EXPORTS),
            status_label=status_label
        )
        pinellas_instance.run()
        status_label.configure(text="Ready to search.")

    def clear_inputs(self):
        for field_reference in self.entry_fields_list:
            field_reference.delete(0, 'end')
        self.search_button_greyscale_source_image = Image.open(self.images_path + "search_button_greyscale.png")
        self.search_button_greyscale_image = ImageTk.PhotoImage(self.search_button_greyscale_source_image)
        self.search_button.configure(image=self.search_button_greyscale_image)
        self.search_button.config(command=lambda: self.do_nothing)
        self.status.configure(text="Ready to search.")

    def open_reports_folder(self):
        print('activated')
        subprocess.call("explorer " + self.reports_path, shell=True)

    ##########
    ##########

    def create_core_window(self):
        self.root = tk.Tk()
        self.root.title("Guerillo")
        self.root.iconbitmap(self.images_path + 'phone.ico')
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
        self.username_field.bind('<Return>',self.enter_login)

        # PW label and field
        self.password_label = tk.Label(self.login_elements_frame, bg="white", text="Password", font=("Constantia", 12))
        self.password_label.grid(row=2, column=0 )
        self.password_field = tk.Entry(self.login_elements_frame, width=22, show="*")
        self.password_field.bind('<Return>',self.enter_login)
        self.password_field.grid(row=3, column=0)
        # login button
        self.login_button_source_image = Image.open(self.images_path + "login_button.png")
        self.login_button_image = ImageTk.PhotoImage(self.login_button_source_image)
        self.login_button = tk.Button(self.login_elements_frame,
                                      borderwidth=0,
                                      highlightthickness=0,
                                      image=self.login_button_image,
                                      text="     Login     ",
                                      command=lambda: self.login())
        self.login_button.grid(row=4, columnspan=2)
        #spacer TODO: get a canvas line in here or something
        # self.spacer_label = tk.Label(self.login_elements_frame,bg="white",text="  ")
        # self.spacer_label.grid(row=,column=0)
        #sign up option TODO: replace with button??
        self.sign_up_label = tk.Label(self.login_elements_frame,bg="white",text="Sign up")
        self.sign_up_label.grid(row=5,column=0)
        #TODO: give signup functionality


        #login status label
        self.login_status_label = tk.Label(self.login_elements_frame,bg="white",font=("Constantia",12))
        self.login_status_label.grid(row=6,column=0,pady=5)

    def create_logo(self):
        self.logo = ImageTk.PhotoImage(Image.open(self.images_path + "pano.png"))
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
        self.file_menu.add_command(label="New Search / Clear Page", command=lambda: self.clear_inputs())  # TODO: check if we dont need lamba anymore
        self.file_menu.entryconfig(0, state=tc.DISABLED)
        self.file_menu.add_command(label="Open Reports Folder", command=lambda: self.open_reports_folder())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.root.destroy)

    def create_account_menu(self):
        self.account_menu = tk.Menu(self.top_menu, tearoff=False)
        self.top_menu.add_cascade(label="Account", menu=self.account_menu)
        self.account_menu.add_command(label="Account Options", command=lambda: self.do_nothing())
        self.account_menu.add_command(label="Sign Out", command=lambda: self.sign_out())

    def create_entry_grid(self):
        # build entry grid frame (grid layout for text entry components and search button)
        self.entry_grid_frame = tk.Frame(self.search_screen, bg="white")
        self.entry_grid_frame.place(in_=self.search_screen, anchor="c", relx=.50, rely=.45)

    def inject_lower_bound_elements(self, grid_target, row_placement):
        self.lower_bound_label = tk.Label(grid_target, bg="white", text="Min Mortgage Amount", font=("Constantia", 12))
        self.lower_bound_label.grid(row=row_placement, column=0, sticky=tc.E, pady=5)
        self.lower_bound_input = tk.Entry(grid_target, width=15, font="Calibri 13")
        self.lower_bound_input.bind("<Key>", self.activate_search_button)
        self.lower_bound_input.grid(row=row_placement, column=1)
        self.entry_fields_list.append(self.lower_bound_input)

    def inject_upper_bound_elements(self, grid_target, row_placement):
        self.upper_bound_label = tk.Label(grid_target, bg="white", text="Max Mortgage Amount", font=("Constantia", 12))
        self.upper_bound_label.grid(row=row_placement, column=0, sticky=tc.E, pady=5)
        self.upper_bound_input = tk.Entry(grid_target, width=15, font="Calibri 13")
        self.upper_bound_input.grid(row=row_placement, column=1)
        self.upper_bound_input.bind("<Key>", self.activate_search_button)
        self.entry_fields_list.append(self.upper_bound_input)

    def inject_start_date_elements(self, grid_target, row_placement):
        self.start_date_label = tk.Label(grid_target, bg="white", text="Start Date", font=("Constantia", 12))
        self.start_date_label.grid(row=row_placement, column=0, sticky=tc.E, pady=5)
        self.start_date_input = tk.Entry(grid_target, width=15, font="Calibri 13")
        self.start_date_input.grid(row=row_placement, column=1)
        self.start_date_input.bind("<Key>", self.activate_search_button)
        self.entry_fields_list.append(self.start_date_input)

    def inject_end_date_elements(self, grid_target, row_placement):
        self.end_date_label = tk.Label(grid_target, bg="white", text="End Date", font=("Constantia", 12))
        self.end_date_label.grid(row=row_placement, column=0, sticky=tc.E, pady=5)
        self.end_date_input = tk.Entry(grid_target, width=15, font="Calibri 13")
        self.end_date_input.grid(row=row_placement, column=1)
        self.end_date_input.bind("<Key>", self.activate_search_button)
        self.end_date_input.bind("<Return>",self.enter_search)
        self.entry_fields_list.append(self.end_date_input)

    def inject_search_button(self, grid_target, row_placement):
        self.search_button_greyscale_image = ImageTk.PhotoImage(
            Image.open(self.images_path + "search_button_greyscale.png"))
        self.search_button = tk.Button(grid_target,
                                       text="Search",
                                       image=self.search_button_greyscale_image,
                                       highlightthickness=0,
                                       borderwidth=0
                                       )
        self.search_button.grid(row=row_placement, column=0, columnspan=2, pady=10)

    def inject_county_dropdown(self, grid_target, row_placement):
        self.county_dropdown_label = tk.Label(grid_target, bg="white", text="County to Search", font=("Constantia", 12))
        self.county_dropdown_label.grid(row=row_placement, column=0, sticky=tc.E)
        counties = self.user.keychain.get_connected_items()
        counties_list = []
        for county in counties:
            counties_list.append(county.county_name)
        self.county_options = counties_list
        self.variable = tk.StringVar(grid_target)
        self.variable.set(self.county_options[0])
        self.county_dropdown = tk.OptionMenu(grid_target, self.variable, *self.county_options)
        self.county_dropdown.grid(row=row_placement, column=1)
        #self.county_dropdown.configure(state="disabled")

    def inject_guerillo_header(self, grid_target, row_placement):
        self.guerillo_header = tk.Label(grid_target, bg="white", text="Guerillo", font=("Constantia", 40))
        self.guerillo_header.grid(row=row_placement, column=0, columnspan=2, pady=3)

    def inject_search_query_elements(self, grid_target, row_count):
        self.inject_search_button(grid_target, row_count - 1)  # has to be first b/c it needs to exist before creating
        # the upcoming textfields
        self.inject_guerillo_header(grid_target, row_count - 7)
        #self.inject_county_dropdown(grid_target, row_count - 6)
        self.inject_lower_bound_elements(grid_target, row_count - 5)
        self.inject_upper_bound_elements(grid_target, row_count - 4)
        self.inject_start_date_elements(grid_target, row_count - 3)
        self.inject_end_date_elements(grid_target, row_count - 2)

    def __init__(self):
        self.user = None

        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.reports_path = self.root_path + "\\bin\\reports\\"
        self.images_path = self.root_path + "\\res\\img\\"

        self.create_core_window()
        self.create_main_frame()
        self.create_search_screen()
        self.create_logo()
        self.create_status_bar()
        self.create_top_menu()
        self.create_entry_grid()
        self.inject_search_query_elements(self.entry_grid_frame, 7)
        self.search_screen.grid_remove()
        self.create_login_screen()

        self.root.mainloop()
