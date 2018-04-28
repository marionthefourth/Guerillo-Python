# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:57:50 2018

@author: Kenneth

Table of Contents:

"""
from tkinter import *
import tkinter as tk
import tkinter.messagebox as msg
from PIL import Image,ImageTk
import webbrowser



""" Methods"""
def doNothing():
    print("would have done something")
def linkToPano(event):
    webbrowser.open_new(r"http://www.panoramic.global")

inputValue = ""
def retrieve_input(tB):
    global inputValue
    inputValue = tB.get("1.0","end-1c")
    tB.delete(1.0,END)
    return inputValue
def display_input():
    adjustaLabel.configure(text=inputValue)
    
    
"""end of Methods"""



""" Main Window Setup """

#basic core window setup
root = tk.Tk()
root.title("Guerillo")
root.iconbitmap('phone.ico')
root.geometry('800x500') #syntax is 'WidthxHeight'
root.config(background="white")


#create status bar
statusFrame = Frame(root)
statusFrame.pack(side=BOTTOM, fill=X)
status = Label (statusFrame, text="Ready to search.", bd=1,relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

#create main frame (wherein a grid will be used) - color is for help while working and should be removed
mF = Frame(root, bg="yellow")
mF.pack(side=TOP,fill=BOTH,expand=1)


#get logo and scale it down
sourceImage = Image.open("pano.png")
sourceImage = sourceImage.resize((int(sourceImage.width/2),int(sourceImage.height/2)))
logo = ImageTk.PhotoImage(sourceImage)


#get logo embedded at bottom right corner
logoLabel = tk.Label(root, image=logo, highlightthickness = 0, borderwidth = 0, cursor="hand2", anchor=E)
logoLabel.image=logo
logoLabel.place(rely=1.0, relx=1.0, x=-11, y=-20, anchor=SE)
logoLabel.bind("<Button-1>",linkToPano)


#create basic menu
topMenu = Menu(root)
root.config(menu=topMenu)
#add a file dropdown menu
fileMenu = Menu(topMenu,tearoff=False)
topMenu.add_cascade(label="File",menu=fileMenu)
fileMenu.add_command(label="New Search / Clear Page", command=doNothing)
fileMenu.add_separator()
fileMenu.add_command(label="Quit", command=root.destroy)


""" end of main window setup """

""" Entry Grid Setup """
#build Entry Grid Frame
egF = Frame(mF, bg="purple")
egF.pack(side=LEFT,fill=BOTH)
egF.columnconfigure(2,minsize=75)


#build first column of grid with entry box and display area
entryBox = Text(egF, height=2,width=10)
entryBox.grid(row=0,column=0)
adjustaLabel= Label(egF,bg="blue")
adjustaLabel.grid(row=1,column=0,sticky=N+S+E+W)

#build second column of grid with command buttons
buttonCommit=Button(egF,height=1,width=10, text="Commit",command=lambda:retrieve_input(entryBox))
buttonCommit.grid(row=0,column=1,columnspan=2,sticky=E+W,padx=10)
colorLabel = Label(egF,bg="grey")
colorLabel.grid(row=1,column=1,columnspan=2,sticky=N+S+E+W)
buttonPrint=Button(egF,height=1,width=10,text="Print",command=lambda:display_input())
buttonPrint.grid(row=1,column=1,columnspan=2,sticky=E+W,padx=10)
""" end of entry grid setup """

root.mainloop()