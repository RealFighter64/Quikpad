import tkinter as tk
import tkinter.ttk as ttk

from application import Application
from config import LanguageConfig

window = tk.Tk()
window.title("Quikpad")
window.minsize(750, 500)
window.geometry("750x500")

style = ttk.Style()
print(style.theme_names())
style.theme_use('vista')

config = LanguageConfig.fromFile("languages.json")

app = Application(window, config)
app.pack(fill='both', expand=1)

menu = tk.Menu(window)
menu_file = tk.Menu(menu, tearoff=0)
menu_file.add_command(label="New", command=app.file_new, accelerator="Ctrl-N")
menu_file.add_command(label="Save", command=app.file_save, accelerator="Ctrl-S")
menu_file.add_command(label="Save As", command=app.file_save_as, accelerator="Ctrl-Shift-S")
menu_file.add_command(label="Open", command=app.file_open, accelerator="Ctrl-O")
menu_file.add_command(label="Run", command=app.file_run, accelerator="Ctrl-R")
menu.add_cascade(label="File", menu=menu_file)

menu_window = tk.Menu(menu, tearoff=0)
menu_window.add_command(label="New Pane", command=app.window_new_pane, accelerator="Ctrl-P")
menu.add_cascade(label="Window", menu=menu_window)
window.config(menu=menu)

# File
window.bind_all("<Control-n>", app.file_new)
window.bind_all("<Control-s>", app.file_save)
window.bind_all("<Control-Shift-S>", app.file_save_as)
window.bind_all("<Control-o>", app.file_open)
window.bind_all("<Control-r>", app.file_run)

# Window
window.bind_all ("Control-p", app.window_new_pane)

window.mainloop()