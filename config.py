import json

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font

from pygments.lexers import get_lexer_by_name

class FontConfig:
    def __init__(self):
        print(font.names())
        self.normalFont = font.nametofont("TkFixedFont").copy()
        self.boldFont = self.normalFont.copy()
        self.boldFont.config(weight="bold")
        self.italicFont = self.normalFont.copy()
        self.italicFont.config(slant="italic")
        self.boldItalicFont = self.normalFont.copy()
        self.boldItalicFont.config(weight="bold", slant="italic")

class LanguageConfig:
    def __init__(self):
        self.fonts = FontConfig()
        self.languages = {}

    def fromFile(filename):
        try:
            with open(filename, "r") as configfile:
                config = LanguageConfig()
                config.languages = json.load(configfile)
                return config
        except FileNotFoundError:
            print("File not found: " + filename)
    
    def toFile(self, filename):
        with open(filename, "w") as configfile:
            json.dump(self.languages, configfile, indent=4)

    def getLanguage(self, language):
        return self.languages[language]
    
    def editLanguage(self, language, **kwargs):
        self.languages[language] = kwargs
    
    def getToken(self, language, token):
        return self.languages[language]["tokens"][token]

    def setUpTags(self, language, textWidget):
        for key, token in self.languages[language]["tokens"].items():
            if token["bold"]:
                if token["italic"]:
                    font = self.fonts.boldItalicFont
                else:
                    font = self.fonts.boldFont
            else:
                if token["italic"]:
                    font = self.fonts.italicFont
                else:
                    font = self.fonts.normalFont
            textWidget.tag_config(key, foreground=token["fg"], font=font)