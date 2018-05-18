import tkinter as tk
import tkinter.constants as tc

from PIL import Image, ImageTk

from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.user import User
from guerillo.config import Resources
from guerillo.threads.signup_thread import SignupThread
from guerillo.ui.screen import Screen
from guerillo.utils.file_storage import FileStorage


class AuthenticationScreen(Screen):

    def enter_login(self, event):
        self.login()

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
            self.login_status_label.configure(text="Login successful! Loading search functions.", fg="green")
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
