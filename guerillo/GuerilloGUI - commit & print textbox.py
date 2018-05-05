# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:57:50 2018

@author: Kenneth

Table of Contents:

"""
import tkinter.constants as tc
import tkinter as tk
import time
import tkinter.messagebox as msg
from PIL import Image,ImageTk
import webbrowser
import os
import guerillo.pinellas as pinellas
from threading import Thread

class SecondaryThread(Thread):
    fields_list = []
    status_label = None
    def run(self):
        retrieve_inputs_and_run(self.fields_list,self.status_label)



""" Methods"""
def do_nothing():
    print("would have done something")
def link_to_pano(event):
    webbrowser.open_new(r"http://www.panoramic.global")

output_list = []
def search_button_method(passed_fields_list,passed_status_label):
    search_thread = SecondaryThread()
    search_thread.status_label = passed_status_label
    search_thread.fields_list = passed_fields_list
    search_thread.start()


def retrieve_inputs_and_run(fields_list,status_label):
    global output_list
    output_list = []
    for field_reference in fields_list:
        output_list.append(field_reference.get("1.0", "end-1c"))
    print(output_list)
    pinellas_instance = pinellas.Pinellas(status_label)
    pinellas_instance.run(output_list)
    status_label.configure(text="Ready to search.")
    return output_list

def clear_inputs(fields_list):
    for field_reference in fields_list:
        print(field_reference.get("1.0", "end-1c"))
        field_reference.delete('1.0', tc.END)

    
    
"""end of Methods"""

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
images_path = root_path + "\\res\\img\\"

""" Main Window Setup """

#basic core window setup
root = tk.Tk()
root.title("Guerillo")
root.iconbitmap(images_path + 'phone.ico')
root.geometry('500x300') #syntax is 'WidthxHeight'
root.config(background="white")



#create status bar
status_frame = tk.Frame(root)
status_frame.pack(side=tc.BOTTOM, fill=tc.X)
status = tk.Label (status_frame, text="Ready to search.", bd=1, relief=tc.SUNKEN, anchor=tc.W)
status.pack(side=tc.BOTTOM, fill=tc.X)


#create main frame (wherein a grid will be used) - color is for help while working and should be removed
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tc.TOP, fill=tc.BOTH, expand=1)


#get logo and scale it down
pano_source_image = Image.open(images_path + "pano.png")
#pano_source_image = pano_source_image.resize((int(pano_source_image.width / 2), int(pano_source_image.height / 2)))
logo = ImageTk.PhotoImage(pano_source_image)


#get logo embedded at bottom right corner
logo_label = tk.Label(root, image=logo, highlightthickness = 0, borderwidth = 0, cursor="hand2", anchor=tc.E)
logo_label.image=logo
logo_label.place(rely=1.0, relx=1.0, x=-11, y=-20, anchor=tc.SE)
logo_label.bind("<Button-1>", link_to_pano)


#create basic menu
top_menu = tk.Menu(root)
root.config(menu=top_menu)
#add a file dropdown menu
file_menu = tk.Menu(top_menu, tearoff=False)
top_menu.add_cascade(label="File", menu=file_menu)



""" end of main window setup """

""" Entry Grid Setup """
entry_fields_list = []
#build entry grid frame (grid layout for text entry components and search button)
entry_grid_frame = tk.Frame(main_frame, bg="white")
entry_grid_frame.pack(side=tc.LEFT, fill=tc.BOTH)
entry_grid_frame.columnconfigure(3, minsize=75)


#build column elements (labels, text inputs, search button)
lower_bound_label = tk.Label(entry_grid_frame,bg="white",text="Minimum Mortgage Amount")
lower_bound_label.grid(row=0,column=0,sticky=tc.E)
lower_bound_input = tk.Text(entry_grid_frame, height=1, width=10)
lower_bound_input.grid(row=0,column=1)
entry_fields_list.append(lower_bound_input)

upper_bound_label = tk.Label(entry_grid_frame,bg="white",text="Maximum Mortgage Amount")
upper_bound_label.grid(row=1,column=0,sticky=tc.E)
upper_bound_input = tk.Text(entry_grid_frame, height=1, width=10)
upper_bound_input.grid(row=1,column=1)
entry_fields_list.append(upper_bound_input)

start_date_label = tk.Label(entry_grid_frame,bg="white",text="Start Date")
start_date_label.grid(row=2,column=0,sticky=tc.E)
start_date_input = tk.Text(entry_grid_frame, height=1, width=10)
start_date_input.grid(row=2,column=1)
entry_fields_list.append(start_date_input)

end_date_label = tk.Label(entry_grid_frame,bg="white",text="End Date")
end_date_label.grid(row=3,column=0,sticky=tc.E)
end_date_input = tk.Text(entry_grid_frame, height=1, width=10)
end_date_input.grid(row=3,column=1)
entry_fields_list.append(end_date_input)

search_button=tk.Button(entry_grid_frame, height=2, width=10, text="Search", command=lambda:search_button_method(entry_fields_list,status))
search_button.grid(row=1,column=2,columnspan=2,rowspan=2,sticky=tc.E+tc.W,padx=10)

#have to add this section here because thsi is all done in-line.
#if done above where it makes more sense, the entry_fields_list variable doesn't exist yet
#this can be handled more appropriately once the class is created and things are instantiated...maybe?
file_menu.add_command(label="New Search / Clear Page",command=lambda:clear_inputs(entry_fields_list))
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.destroy)

""" end of entry grid setup """

root.mainloop()