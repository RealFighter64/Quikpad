from cx_Freeze import Executable, setup
import os

os.environ['TCL_LIBRARY'] = "C:\\Program Files (x86)\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Program Files (x86)\\Python36-32\\tcl\\tk8.6"

setup(
    name = "Quikpad",
    version = "1.0",
    author = "William Gooch",
    author_email = "Omitted",
    options={
        "build_exe": {
            "packages": ["tkinter", "pygments"],
            "include_files": [
                "languages.json",
                "C:\\Program Files (x86)\\Python36-32\\DLLs\\tcl86t.dll", "C:\\Program Files (x86)\\Python36-32\\DLLs\\tk86t.dll"
            ]
        }
    },
    executables=[Executable("main.py", icon="favicon.ico",)]
)