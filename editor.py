import os
import subprocess

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.font as font

from pygments import lex
from pygments.lexers import PythonLexer

class Editor(ttk.Frame):
    def __init__(self, root, filename, config, *args, **kwargs):
        ttk.Frame.__init__(self, root, *args, **kwargs)
        self.filename = filename
        self.language = "python"
        self.savedFileContents = ""
        self._resetting_modified_flag = False
        self.config = config

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.horizontalScrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.verticalScrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        self.text = tk.Text(self, bd=0, wrap=tk.NONE, xscrollcommand=self.horizontalScrollbar.set, yscrollcommand=self.setVertical)
        self.text.grid(row=0, column=1, sticky=tk.NSEW)
        self.text.bind("<<Modified>>", self._textModified);

        self.lineNumbers = tk.Text(self, bd=0, wrap=tk.NONE, state=tk.DISABLED, width=4, bg="#CCDDDD", yscrollcommand=self.setVertical)
        self.lineNumbers.grid(row=0, rowspan=2, column=0, sticky=tk.NSEW)

        self.horizontalScrollbar.config(command=self.scrollHorizontal)
        self.horizontalScrollbar.grid(row=1, column=1, sticky=tk.NSEW)

        self.verticalScrollbar.config(command=self.scrollVertical)
        self.verticalScrollbar.grid(row=0, column=2, sticky=tk.NSEW)

        self.text.bind("<Tab>", self.tab);
        self.text.bind("<BackSpace>", self.backspace)
        self.text.bind("<Return>", self.enter)
        #self.text.bind("<space>", self.setTags);

        self.tagConfig();
        self.populateLineNumbers();

    def scrollHorizontal(self, action, position, type=None):
        self.text.xview_moveto(position)

    def scrollVertical(self, action, position, type=None):
        self.text.yview_moveto(position)
        self.lineNumbers.yview_moveto(position)

    def setVertical(self, first, last):
        self.text.yview_moveto(first)
        self.lineNumbers.yview_moveto(first)
        self.verticalScrollbar.set(first, last)

    def tab(self, *args):
        self.text.insert(tk.INSERT, " " * 4)
        return 'break'
    def backspace(self, *args):
        validChars = set(' ')
        text = self.text.get("insert linestart", "insert")
        if(all(char in validChars for char in text)):
            if(len(text) % 4 == 0 and len(text) != 0):
                # Delete 4 spaces
                self.text.delete("insert-4c", "insert")
                return 'break'
    
    def enter(self, *args):
        text = self.text.get("insert linestart", "insert")
        isColon = self.text.get("insert-1c") == ":"
        c = 0
        if isColon: 
            c += 4
        print("thing")
        for char in text:
            if char == ' ':
                c += 1
            else:
                break
        if c % 4 == 0:
            self.text.insert("insert", "\n" + (' ' * c))
            return 'break'
    def tagConfig(self):
        self.config.setUpTags(self.language, self.text)

    def setTags(self, *args):
        self.text.mark_set("range_start", "1.0");
        data = self.text.get("1.0", 'end-1c')
        for tagName in self.text.tag_names():
            self.text.tag_remove(tagName, "1.0", "end")
        for token, content in lex(data, PythonLexer()):
            self.text.mark_set("range_end", "range_start + %dc" % len(content))
            self.text.tag_add(str(token), "range_start", "range_end")
            #print(token)
            self.text.mark_set("range_start", "range_end")
        #print()

    def populateLineNumbers(self):
        self.lineNumbers.config(state=tk.NORMAL)
        self.lineNumbers.delete("1.0", tk.END)
        for i in range(1, len(self.text.get("1.0", 'end').split("\n"))):
            self.lineNumbers.insert(tk.END, str(i) + "\n")
        self.lineNumbers.config(state=tk.DISABLED)

    def _textModified(self, *args):
        #scrollPositionA, scrollPositionB = self.verticalScrollbar.get()
        if(not self._resetting_modified_flag):
            self.textModified(args)
        #self.setVertical(scrollPositionA, scrollPositionB)
        self.text.see("insert")
    def textModified(self, *args):
        self._resetting_modified_flag = True
        try:
            self.text.tk.call(self.text._w, 'edit', 'modified', 0)
        finally:
            self._resetting_modified_flag = False
        
        self.setTags()
        self.populateLineNumbers()
        if self.unsaved():
            self.showUnsaved()
    def showUnsaved(self):
        if "*" not in self.master.tab(self, option="text"):
            self.master.tab(self, text=self.master.tab(self, option="text")+" *")
    def save_as(self):
        self.savedFileContents = self.text.get("1.0", 'end-1c')
        tempFile = filedialog.asksaveasfile()
        self.filepath = tempFile.name
        self.filename = os.path.basename(self.filepath)
        tempFile.write(self.savedFileContents)
        tempFile.close()
        self.master.tab(self, text=self.filename)

    def save(self):
        try:
            self.savedFileContents = self.text.get("1.0", 'end-1c')
            tempFile = open(self.filepath, "w")
            tempFile.write(self.savedFileContents)
            tempFile.close()
            self.master.tab(self, text=self.filename)
        except AttributeError:
            self.save_as()
    
    def open(self):
        tempFilename = filedialog.askopenfilename()
        try:
            self.load(tempFilename)
        except FileNotFoundError:
            self.master.forget("current")

    def load(self, filepath):
        self.filepath = filepath;
        self.filename = os.path.basename(self.filepath)
        tempFile = open(self.filepath, "r")
        self.savedFileContents = tempFile.read();
        tempFile.close()
        self.text.delete("1.0", 'end-1c')
        self.text.insert("1.0", self.savedFileContents);
        self.master.tab(self, text=self.filename)
    def run(self):
        if(self.close()):
            os.system("start cmd /k python " + self.filepath);
    def unsaved(self):
        return self.text.get("1.0", 'end-1c') != self.savedFileContents
    def close(self):
        if(self.unsaved()):
            save = messagebox.askyesnocancel("Save unsaved file?", "Your file is unsaved. Do you want to save it?") 
            if(save == True):
                self.save()
                return True
            elif(save == None):
                return False
            else:
                return True
        else:
            return True