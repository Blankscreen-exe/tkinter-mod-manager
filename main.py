from tkinter import Tk, ttk, filedialog, Frame, StringVar
from tkinter import Listbox
from pprint import pprint as pp
from functions import *
import os
import json
import platform

class config:
    source_folder = "/externalvolumes/Hammad/tkinter_practice/mod_dl/"
    destination_folder = "/externalvolumes/Hammad/tkinter_practice/mod_loaded/"


# Sample items lists (replace with your data source)
items_lists = [[], []]

items_lists[0] = get_folder_names(config.source_folder)

# for index in range(20):
#   items_lists[0].append(f'Item A - {index}')
#   items_lists[1].append(f'Item B - {index}')


# Function to handle listbox selection (replace with your logic)
# def handle_selection(event, listbox_type):
#     selected_index = event.widget.curselection()[0]
#     selected_item = event.widget.get(selected_index)
#     mod_folder_path = os.path.join(config.source_folder)
#     print(mod_folder_path)
#     items_lists[1] = get_folder_contents(mod_folder_path)[selected_index]["files"]
#     print(items_lists[1])

#     print(
#         f"Selected item in listbox {listbox_type}: {selected_item} mit {selected_index}"
#     )

#     # TODO: Update the target listbox based on the selection
#     target_listbox.delete(0, tk.END)  # Clear target listbox first (optional)
#     # Add new items to the target listbox based on selected item or logic
#     target_listbox.insert("end", "New Item 1 based on", selected_item)
#     target_listbox.insert("end", "New Item 2 based on", selected_item)

# BOOKMARK: scroll listbox


class ScrollableListbox(Frame):
    def __init__(self, master, items, width=50, height=10, selectmode="browse"):
        super().__init__(master)
        self.master = master

        # Listbox
        self.listbox = Listbox(self, selectmode=selectmode, width=width, height=height)
        for item in items:
            self.listbox.insert("end", item)
        self.listbox.grid(column=0, row=0)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.listbox.yview
        )
        self.scrollbar.grid(column=1, row=0)

        # Link scrollbar and listbox
        self.listbox.config(yscrollcommand=self.scrollbar.set)


# BOOKMARK: BUTTON OPTIONS


class ButtonBar(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        button = ttk.Button(self, text=" Refresh List ", style="Custom1.TButton")
        button.grid(column=0, row=0, sticky="n", padx=3)
        button = ttk.Button(self, text="  Install Mod  ", style="Custom1.TButton")
        button.grid(column=0, row=1, sticky="n", padx=3)
        button = ttk.Button(self, text="Uninstall Mod", style="Custom1.TButton")
        button.grid(column=0, row=2, sticky="n", padx=3)


# BOOKMARK: LISTBOX 2


class ListBoxFrame2(Frame):
    def __init__(self, master, title_text, items_list):
        super().__init__(master)  # Call parent constructor
        self.master = master

        # Create title label
        self.title_label = ttk.Label(
            self, text=title_text, font=("TkDefaultFont", 12, "bold")
        )
        self.title_label.grid(column=0, columnspan=2, row=0)

        # Create listbox
        self.listbox2 = Listbox(self, height=5, selectmode="multiple")
        for item in items_list:
            self.listbox2.insert("end", item)
        self.listbox2.bind(
            "<<ListboxSelect>>", lambda event: handle_selection(event, "mod-file-list")
        )
        self.listbox2.grid(column=0, columnspan=2, row=1, rowspan=5, ipadx=7)

        # Create buttons dynamically
        button_texts = ["Select All", "De-Select All"]
        for i, text in enumerate(button_texts):
            button = ttk.Button(self, text=text, style="Custom1.TButton")
            button.grid(column=i, row=6)  # Adjust grid options


# BOOKMARK: LISTBOX 1


class ListBoxFrame1(Frame):
    def __init__(self, master, title_text, items_list, full_height=False):
        super().__init__(master)  # Call parent constructor
        self.master = master

        # Create title label
        self.title_label = ttk.Label(
            self, text=title_text, font=("TkDefaultFont", 12, "bold")
        )
        self.title_label.grid(column=0, columnspan=2, row=0)

        # Create listbox
        self.listbox1 = Listbox(self, selectmode="browse")
        for item in items_list:
            self.listbox1.insert("end", item)
        self.listbox1.bind(
            "<<ListboxSelect>>",
            lambda event: handle_selection(event, "mod-folder-list"),
        )
        if full_height:
            self.listbox1.grid(
                column=0, columnspan=2, row=1, rowspan=5, sticky="n"
            )  # Adjust for full height
        else:
            self.listbox1.grid(
                column=0, columnspan=2, row=1, rowspan=2
            )  # Adjust for partial height

    def populate_list(self):
        pass


# MSG: Settings tab


class FolderPathEntry(Frame):
    def __init__(self, master, label_text, variable, browse_command):
        super().__init__(master)  # Call parent constructor
        self.master = master

        # Label for folder path
        self.folder_label = ttk.Label(self, text=label_text)
        self.folder_label.grid(column=0, columnspan=2, row=0)

        # Input box for folder path
        self.folder_entry = ttk.Entry(
            self, textvariable=variable, width=25
        )  # Adjust width as needed
        self.folder_entry.grid(column=2, columnspan=3, row=0, padx=15)

        # Browse button
        self.browse_button = ttk.Button(
            self,
            text="Browse",
            style="Custom1.TButton",
            command=lambda: browse_command(variable),
        )
        self.browse_button.grid(column=6, row=0)


# -----------------------------------------------------------------


class ModManager:
    def __init__(self):

        # Constants
        self.app_title = 'Mod Manager'
        self.app_window_size = "440x220"
        self.config_file_name = 'modmanager_config.json'
        self.app_base_dir = os.getcwd()
        self.os_is_windows = platform.system() == "Windows"

        self.read_config()

        self.root = Tk()
        self.root.title(self.app_title)
        self.root.geometry(self.app_window_size)
        self.root.resizable(False, False)

        self.get_styles()

        # Create the notebook (tabs container)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(column=0, columnspan=6, row=0, rowspan=6)

        # Create frames for each tab
        self.manage_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.manage_frame, text="Manage")
        self.notebook.add(self.settings_frame, text="Settings")

        # MSG: Manage tab layout

        self.manage_content_frame = ttk.Frame(self.manage_frame)
        self.manage_content_frame.grid(column=0, columnspan=6, row=0, rowspan=6)

        self.right_frame = ButtonBar(
            self.manage_content_frame, ["Refresh List", "Install Mod", "Uninstall Mods"]
        )
        self.right_frame.grid(column=6, row=0, rowspan=6)

        self.listbox_frame_2 = ListBoxFrame2(
            self.manage_content_frame, "Mod Files", items_lists[1]
        )
        self.listbox_frame_2.bind("<Button>", self.handle_file_selection)
        self.listbox_frame_2.grid(column=2, columnspan=2, row=0, rowspan=6, sticky="n")

        self.listbox_frame_1 = ListBoxFrame1(
            self.manage_content_frame, "Mod List", items_lists[0], full_height=True
        )
        self.listbox_frame_1.bind("<Button>", self.handle_folder_selection)
        self.listbox_frame_1.grid(column=0, columnspan=2, row=0, rowspan=6)

        self.source_folder_path_var = StringVar()
        self.source_folder_entry = FolderPathEntry(
            self.settings_frame,
            "Source Folder        ",
            self.source_folder_path_var,
            self.handle_browse,
        )
        self.source_folder_entry.grid(column=0, columnspan=6, row=0)

        self.destination_folder_path_var = StringVar()
        self.destination_folder_entry = FolderPathEntry(
            self.settings_frame,
            "Destination Folder",
            self.destination_folder_path_var,
            handle_browse,
        )
        self.destination_folder_entry.grid(column=1, columnspan=6, row=1)

        # Run the main loop
        self.root.mainloop()

    def handle_folder_selection(self, event):
        selected_index = event.widget.curselection()[0]
        selected_item = event.widget.get(selected_index)

    def handle_file_selection(self, event):
        selected_index = event.widget.curselection()[0]
        selected_item = event.widget.get(selected_index)

    def get_base_dir(self):
        return self.app_base_dir

    def handle_browse(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            folder_path_var.set(selected_folder)

    def read_config(self):
        try:
          with open(self.config_file_name, 'r', encoding='utf-8') as f:
            self.app_config = json.load(f)
        except FileNotFoundError:
          # If file not found, create it with default data
          with open(self.config_file_name, 'w', encoding='utf-8') as f:
            json.dump(self.get_config_template(), f, indent=4)
          self.app_config = self.get_config_template()

        return self.app_config

    def write_config(self, key, data):
        keys = key.split('.')
        config = self.read_config()
        d = config
        for k in keys[:-1]:
            d = d[k]
        d[keys[-1]] = data
        with open(os.path.abspath(self.app_config), "w") as file:
            json.dump(config, file)

    def set_source_folder_path(self, path):
        # self.app_config['source_folder_path'] = os.path.join(self.app_base_dir, path.strip('.')) if path.startswith('.') else path
        # if self.os_is_windows:
        #     source_path = os.path.join(self.app_base_dir, *filter(lambda x: x is not '', path.strip('.').split('\\'))) 
        # else:
        #     source_path = os.path.join(self.app_base_dir, *filter(lambda x: x is not '', path.strip('.').split('/'))) 
        
        if not os.path.isabs(path):
            raise ValueError('Path should be absolute not relative.')
        
        self.write_config(
            'source_folder_path', 
            path
        )
        # with open(self.config_file_name, 'w', encoding='utf-8') as f:
        #     json.dump(self.get_config_template(), f, indent=4)

    def set_destination_folder_path(self):
        pass


    def get_config_template(self):
        return {
            "source_folder_path": "",
            "destination_folder_path": "",
            "mod_list": [
                # REF: Example mod list item
                # {
                #   "folder_name": "",
                #   "files": []
                # }
            ],
        }

    def refresh_list(self):
        pass

    def install_mods(self, folder_name):
        pass

    def uninstall_mods(self, folder_name):
        pass

    def select_all_files(self, folder_name):
        pass

    def deselect_all_files(self):
        pass

    def get_styles(self):
        button_style = ttk.Style()
        button_style.configure(
            "Custom1.TButton",
            font=("Calibri", 8, "normal"),
            foreground="white",
            background="#278ef0",
            width="11",
        )
        button_style.map(
            "Custom1.TButton",
            foreground=[("active", "!disabled", "black")],
            background=[("active", "!disabled", "#a9d3fa")],
        )
        return


if __name__ == "__main__":
    mm = ModManager()
