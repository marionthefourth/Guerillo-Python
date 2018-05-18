import webbrowser

from PIL import ImageTk, Image

from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.backend_object import BackendType
from guerillo.classes.backend_objects.county import County
from guerillo.classes.backend_objects.search.query import Query
from guerillo.classes.backend_objects.search.result import SearchResultState, Result
from guerillo.classes.scrapers.scraper import Scraper
from guerillo.config import Resources, Folders
from guerillo.threads.search_thread import SearchThread
from guerillo.ui.screen import Screen
from guerillo.utils.file_storage import FileStorage
import tkinter as tk
import tkinter.constants as tc

class ScraperScreen(Screen):

    def activate_search_button(self, event):
        colorize = True
        for field_reference in self.entry_fields_list:
            if field_reference.get() == "":
                colorize = False
                break
        if colorize:
            if not self.search_button_image:
                self.search_button_image = ImageTk.PhotoImage(Image.open(Resources.SEARCH_BUTTON))
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

    def enter_search(self, event):
        self.search_button_method(self.entry_fields_list, self.status)

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

        query = Query(inputs=input_list, user_uid=self.user.uid)

        if query.is_valid():
            self.sanitize_input_fields(query)

            Backend.save(query)
            # Now begin watching after the SearchResult by the UID generated within the SearchQuery

            result_stream = Backend.get().database() \
                .child(Backend.get_type_folder(BackendType.RESULT)) \
                .child(query.twin_uid).stream(self.result_stream_handler)

            scraper = Scraper.get_county_scraper(
                self.pull_spinner_data(),
                query, FileStorage.get_full_path(Folders.EXPORTS),
                status_label
            )
            scraper.run()

            scraper.search_result.change_mode(SearchResultState.DONE)
        else:
            self.status.configure(text=query.invalid_message())

    def result_stream_handler(self, message):
        print(message["event"])  # put
        print(message["path"])  # /-K7yGTTEp7O549EzTYtI
        print(message["data"])  # {'title': 'Pyrebase', "body": "etc..."}
        self.update_county_label(Result(pyre=message["data"]))

    def update_status_via_state(self, search_result):
        if search_result.sr_state == SearchResultState.INITIAL_NUMBERING_RESULTS:
            self.status_label.configure(text="Processing " + str(len(search_result.num_results)) + " items")
        elif search_result.sr_state == SearchResultState.INITIAL_SEARCH_BY_BOOKPAGE:
            self.status_label.configure(
                text="Handling item " + str(len(search_result.uid_list) - 1) + " of " +
                     str(len(search_result.num_results)))
        elif search_result.sr_state == SearchResultState.INITIAL_SEARCH_BY_NAME:
            self.status_label.configure(text="Taking a deeper look for item " +
                                             str(len(search_result.num_results) - 1) +
                                             " of " + str(len(self.search_result.results_copy)))
        elif search_result.sr_state == SearchResultState.INITIAL_ENTRY_CLEANING:
            self.status_label.configure(text="Successfully found " +
                                             str(len(search_result.uid_list)) + " results. Wrapping up.")
        elif search_result.sr_state == SearchResultState.DONE:
            self.status_label.configure(text="Ready to search.")
            # self.status_label.configure(text="Now processing " + str(len(self.search_result.results_copy)) + " items")

    def pull_spinner_data(self):
        return County(state_name="FL", county_name=self.variable.get())

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

    def create_search_screen(self):
        self.search_screen = tk.Frame(self.main_frame, bg="white")
        self.search_screen.grid(row=0, column=0, sticky="nsew")

    def create_account_menu(self):
        self.account_menu = tk.Menu(self.top_menu, tearoff=False)
        self.top_menu.add_cascade(label="Account", menu=self.account_menu)
        # self.account_menu.add_command(label="Account Options", command=lambda: self.do_nothing())
        self.account_menu.add_command(label="Sign Out", command=lambda: self.sign_out())

    def create_entry_grid(self):
        # build entry grid frame (grid layout for text entry components and search button)
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
        self.guerillo_header = tk.Label(grid_target, bg="white", text="Guerillo",
                                        font=("Constantia", 40))  # 40
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