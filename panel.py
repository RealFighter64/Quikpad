import tkinter as tk
import tkinter.ttk as ttk

from editor import Editor

from buttonNotebook import CustomNotebook

class Panel(ttk.Frame):
    def __init__(self, root, config, *args, **kwargs):
        ttk.Frame.__init__(self, root, *args, **kwargs)

        self.config = config

        self.editors = CustomNotebook(self, padding="3p")
        self.editors.pack(fill='both', expand=1)

    def file_new(self, *args):
        tempEditor = Editor(self.editors, "untitled", self.config)
        self.editors.add(tempEditor, text=tempEditor.filename)
        self.update()

    def file_save_as(self, *args):
        tabName = self.editors.select()
        editorWidget = self.editors._nametowidget(tabName)
        editorWidget.save_as()

    def file_save(self, *args):
        tabName = self.editors.select()
        editorWidget = self.editors._nametowidget(tabName)
        editorWidget.save()
    
    def file_open(self, *args):
        tempEditor = Editor(self.editors, "", self.config);
        self.editors.add(tempEditor, text="");
        self.editors.select(tempEditor)
        self.update();
        tempEditor.open();

    def file_run(self, *args):
        tabName = self.editors.select()
        editorWidget = self.editors._nametowidget(tabName)
        editorWidget.run()

    def update(self, *args):
        if len(self.editors.tabs()) <= 0:
            return True
        else:
            return False