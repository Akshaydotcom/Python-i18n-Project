import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, ttk
from main import main_function
from threading import *

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
    

app = tk.Tk()
app.title("i18n Translation Tool")
app.geometry('400x400')

ico = Image.open('p2.png')
photo = ImageTk.PhotoImage(ico)
app.wm_iconphoto(False, photo)

progressbar=ttk.Progressbar(mode='indeterminate')

tk.Label(app, text="Select Source Folder:").grid(row=0,column=2)
folder_path = tk.StringVar()
tk.Entry(app, textvariable=folder_path).grid(row=1, column=3)
tk.Button(app, text="Browse", command=lambda: folder_path.set(filedialog.askdirectory())).grid(row=1,column=2)


tk.Label(app, text="Select Target Language:").grid(row=3,column=2)
supported_languages=['French','German','Mandarin','Hindi','Russian']
language_option = tk.StringVar()
language_option.set(supported_languages[0]) # default value
tk.OptionMenu(app, language_option, *supported_languages).grid(row=3,column=3)

tk.Label(app, text='Select Destination Folder:').grid(row=4, column=2)
dest_path=tk.StringVar()
tk.Entry(app, textvariable=dest_path).grid(row=5,column=3)
tk.Button(app, text="Browse", command=lambda: dest_path.set(filedialog.askdirectory())).grid(row=5,column=2)


# Start button
tk.Button(app, text="Start Translation", command=verify).grid(row=6,column=2)
tk.Button(app, text="Exit", command=app.quit).grid(row=6, column=3)

app.mainloop()
