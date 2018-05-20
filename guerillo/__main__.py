import sys,  os
import tkinter as tk
from tkinter import messagebox
from guerillo.gui import GUI
from guerillo.utils.auto_updater import AutoUpdater

#Functional....
#It should finally be functional....
#*tears of joy*

did_update = AutoUpdater.run()
if did_update:
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    root = tk.Tk()
    root.title("Guerillo")
    root.geometry("100x100")
    root.iconbitmap(path+"\\lib\\res\\img\\phone.ico")
    messagebox.showinfo("Update complete","Finished getting a fresh version of Guerillo.\nRe-open Guerillo to get started!")
else:
    gui = GUI()
