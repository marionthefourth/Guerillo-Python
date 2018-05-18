import sys
from tkinter import messagebox
import esky as esky
import tkinter as tk
from tkinter import ttk


class AutoUpdater:

    @staticmethod
    def handle_esky_status(message):
        progress = None
        if message['status'] == 'downloading':
            progress = int((float(message['received']) / float(message['size'])) * 100)
        elif message['status'] == 'ready':
            progress = 100
        if progress is not None:
            print(progress)
        #progress_bar.step(progress)
            # self.progressBar.setValue(progress)

    @staticmethod
    def run():
        if getattr(sys, "frozen", False):
            updater = esky.Esky(sys.executable, "http://guerillo.com/binaries/")
            if updater.find_update():
                #reply = messagebox.askyesno("Out of date","Update available; would you like to update Guerillo?")
                if True:
                #if reply:
                    # root = tk.Tk()
                    # root.geometry('300x250')
                    # root.title("Downloading Update")
                    # text_label = tk.Label(root, text="Progress:", font=("Constantia", 12))
                    # text_label.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
                    # progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
                    # progress_bar.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
                    # root.mainloop()
                    updater.auto_update()#AutoUpdater.handle_esky_status)
                    #root.destroy()
            else:
                print("No new updates found!")

        else:
            print("App is not frozen!")