import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, ttk
from main import main_function
from threading import *
import customtkinter

def verify():
    folder = folder_path.get()
    language = language_option.get()
    dest_folder=dest_path.get()
    if not folder:
        messagebox.showerror("Error","Choose Source Folder Correctly")
    elif not dest_folder:
        messagebox.showerror("Error","Choose Destination Folder Correctly")
    
    translation_thread = Thread(target=start_translation, args=(folder, language, dest_folder))
    translation_thread.start()

    progressbar.place(x=50, y=200, width=100)
    progressbar.start()
    

def start_translation(folder, language, dest_folder):
    try:
        main_function(folder, language, dest_folder)
        messagebox.showinfo("Success", "Translation Completed!")
    finally:
        progressbar.stop()
        progressbar.place_forget()
    
app = customtkinter.CTk()
app.title("LingoPy")
app.geometry('500x500')
titleFont=customtkinter.CTkFont(family='',size=25)
labelFont=customtkinter.CTkFont(family='',size=15)

progressbar=ttk.Progressbar(mode='indeterminate')
customtkinter.CTkLabel(app,text='LingoPy', font=titleFont).grid(row=0,column=3,pady=20)
# customtkinter.CTkLabel(app,image=titleImage, text='').grid(row=0,column=3,pady=20)

customtkinter.CTkLabel(app, text="Select Source Folder:", font=labelFont).grid(row=2,column=2,pady=10, padx=15)
folder_path = tk.StringVar()
customtkinter.CTkEntry(app, textvariable=folder_path).grid(row=4, column=4,pady=10)
open_File_Directory=customtkinter.CTkButton(app, text="Browse", command=lambda: folder_path.set(filedialog.askdirectory())).grid(row=4,column=2,pady=10)


customtkinter.CTkLabel(app, text="Select Target Language:",font=labelFont).grid(row=6,column=2,pady=10,padx=15)
supported_languages=['French','German','Mandarin','Hindi','Russian']
language_option = tk.StringVar()
language_option.set(supported_languages[0]) # default value
customtkinter.CTkOptionMenu(app, variable=language_option, values=supported_languages).grid(row=6,column=4,pady=10)

customtkinter.CTkLabel(app, text='Select Destination Folder:',font=labelFont).grid(row=7, column=2,pady=10,padx=15)
dest_path=tk.StringVar()
customtkinter.CTkEntry(app, textvariable=dest_path).grid(row=9,column=4,pady=10)
customtkinter.CTkButton(app, text="Browse", command=lambda: dest_path.set(filedialog.askdirectory())).grid(row=9,column=2,pady=10)


# Start button
customtkinter.CTkButton(app, text="Start Translation", command=verify).grid(row=12,column=2,pady=10)
customtkinter.CTkButton(app, text="Exit", command=app.quit).grid(row=14, column=3,pady=10)

app.mainloop()
