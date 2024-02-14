import tkinter as tk
from tkinter import filedialog, messagebox
from main import main_function
def start_translation():
    folder = folder_path.get()
    language = language_option.get()
    dest_path=dest_path.get()
    main_function(folder, language, dest_path)
    messagebox.showinfo("Success", "Translation Completed!")

app = tk.Tk()
app.title("i18n Translation Tool")
app.geometry('400x400')

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
tk.Button(app, text="Start Translation", command=start_translation).grid(row=6,column=2)
tk.Button(app, text="Exit", command=app.quit).grid(row=6, column=3)

app.mainloop()
