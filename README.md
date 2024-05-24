# TKinter Mod Manager

This is a simple mod manager built on [Tkinter](https://docs.python.org/3/library/tk.html). This applet is named mod manager because there are certain games which have an option to add or remove mods by copying/pasting/deleting files from one directory to another. The mod files in questions are named in a non-human-friendly way (e.g. `1234567.mod`), now copying and pasting those files from directory to another will of course work but not when you want to keep track of which files belong to which mod. This applet makes that task easy.

## Features

- select **source folder path** with your downloaded mod files.
- select **destination folder path** in which you want to copy your mod files to.
- has a **select all** and **de-select all** feature which lets you select all/none mod files inside a mod folder.
- **copies** all selected mod files from source to destinations directory.
- can **track**, **target** and **delete** mod files from the destination directory without mixing up names.
- does not delete files from source folder for mod file reusability.

## Dependencies

Uses `Python==3.12` and `Tkinter` which is a built-in dependency. 

## Installation

#### Running it from source

Just run it simply with the following command:

```py
python3 main.py
```

#### Installing it on Windows