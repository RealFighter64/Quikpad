import tkinter as tk
import tkinter.ttk as ttk

from editor import Editor

from panel import Panel

class Application(ttk.Frame):
    def __init__(self, root, config, *args, **kwargs):
        ttk.Frame.__init__(self, root, *args, **kwargs)

        style = ttk.Style()

        self.config = config

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.panels = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panels.pack(fill=tk.BOTH, expand=1)

        self.bind_all("<<NotebookTabClosed>>", self.handleTabClosed)
        
        #self.panels = []
        #self.panels.append(Panel(self))
        #self.panels[0].file_new()
        #self.panels[0].focus_set()
        #self.panels.append(Panel(self))
        #self.panels[1].file_new()
        #self.bind_all("<Control-k>", self.getFocus)

    def window_new_pane(self, *args):
        tempPanel = Panel(self, self.config)
        tempPanel.file_new()
        self.panels.add(tempPanel)
        return tempPanel

    def handleTabClosed(self, evt):
        if evt.widget.master.update():
            self.panels.forget(evt.widget.master)

    def getFocus(self, *args):
        foundIt = False
        current = self.focus_get()
        while not foundIt:
            current = current.master
            if current.__class__ == Panel:
                foundIt = True
                print(foundIt)
                return current
            else:
                print("trying again")
        print()

    def file_new(self, *args):
        if len(self.panels.panes()) <= 0:
            self.window_new_pane()
            return
        self.getFocus().file_new()

    def file_save_as(self, *args):
        self.getFocus().file_save_as()

    def file_save(self, *args):
        self.getFocus().file_save()
    
    def file_open(self, *args):
        if len(self.panels.panes()) <= 0:
            self.window_new_pane().file_open()
            return
        self.getFocus().file_open()

    def file_run(self, *args):
        self.getFocus().file_run()