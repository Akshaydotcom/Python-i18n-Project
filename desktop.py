import tkinter as tk
from tkinter import filedialog, messagebox
from main import main_function
def start_translation():
    folder = folder_path.get()
    language = language_option.get()
    main_function(folder, language)
    messagebox.showinfo("Success", "Translation Completed!")

app = tk.Tk()
app.title("i18n Translation Tool")


tk.Label(app, text="Select Source Folder:").pack()
folder_path = tk.StringVar()
tk.Entry(app, textvariable=folder_path).pack()
tk.Button(app, text="Browse", command=lambda: folder_path.set(filedialog.askdirectory())).pack()


tk.Label(app, text="Select Target Language:").pack()
language_option = tk.StringVar()
language_option.set("french") # default value
tk.OptionMenu(app, language_option, "french", "german", "spanish").pack()

# Start button
tk.Button(app, text="Start Translation", command=start_translation).pack()

app.mainloop()
