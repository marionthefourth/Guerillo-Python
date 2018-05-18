import subprocess
import tkinter as tk
import tkinter.constants as tc

from PIL import ImageTk, Image


from guerillo.classes.backend_objects.user import User
from guerillo.config import Resources
from guerillo.utils.auto_updater import AutoUpdater
from guerillo.utils.file_storage import FileStorage


class Screen:

    user: User

    def create_core_window(self):
        self.root = tk.Tk()
        self.root.title("Geurillo")
        self.root.iconbitmap(FileStorage.get_image(Resources.ICON))
        self.root.geometry('300x250')  # syntax is 'WidthxHeight'
        self.root.resizable(width=False, height=False)
        self.root.config(background="white")

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill=tc.BOTH, expand=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def do_nothing(self):
        print("would have done something")

    def open_reports_folder(self):
        print('activated')
        subprocess.call("explorer " + self.reports_path, shell=True)

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

