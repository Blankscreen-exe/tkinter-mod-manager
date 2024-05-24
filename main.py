from tkinter import Tk, ttk, filedialog, Frame, StringVar, IntVar, Variable, END
from tkinter import Listbox
from pprint import pprint as pp
from functions import *
import os
import json
import platform

# Sample items lists (replace with your data source)
# items_lists = [[], []]

# items_lists[0] = get_folder_names(config.source_folder)

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
    def __init__(self, master, func_refresh_list=None, func_install_mod=None, func_uninstall_mod=None):
        super().__init__(master)
        self.master = master

        button_refresh_list = ttk.Button(self, text=" Refresh List ", style="Custom1.TButton")
        button_refresh_list.bind('<Button>', func_refresh_list)
        button_refresh_list.grid(column=0, row=0, sticky="n", padx=3)

        button_install_mod = ttk.Button(self, text="  Install Mod  ", style="Custom1.TButton")
        button_install_mod.bind('<Button>', func_install_mod)
        button_install_mod.grid(column=0, row=1, sticky="n", padx=3)
        
        button_uninstall_mod = ttk.Button(self, text="Uninstall Mod", style="Custom1.TButton")
        button_uninstall_mod.bind('<Button>', func_uninstall_mod)
        button_uninstall_mod.grid(column=0, row=2, sticky="n", padx=3)


# BOOKMARK: LISTBOX 2


class ListBoxFrame2(Frame):
    def __init__(self, master, func_get_config, item_select_command, select_all_command, deselect_all_command):
        super().__init__(master)  # Call parent constructor
        self.master = master

        self.func_get_config = func_get_config


        # Create title label
        self.title_label = ttk.Label(
            self, text='Mod Files', font=("TkDefaultFont", 12, "bold")
        )
        self.title_label.grid(column=0, columnspan=2, row=0)

        # Create listbox
        self.listbox2 = Listbox(self, height=5, selectmode="multiple")
        
        # REVIEW: do we need to run it here
        # self.reset_file_list()

        self.listbox2.bind(
            "<<ListboxSelect>>", lambda event: item_select_command(event)
        )
        self.listbox2.grid(column=0, columnspan=2, row=1, rowspan=5, ipadx=7)

        # Create buttons dynamically
        button_texts = ["Select All", "De-Select All"]
        
        button_select_all = ttk.Button(self, text="Select All", style="Custom1.TButton")
        button_select_all.bind('<Button>', lambda event: select_all_command(event, self.folder_index))
        button_select_all.grid(column=0, row=6)
        button_deselect_all = ttk.Button(self, text="De-Select All", style="Custom1.TButton")
        button_deselect_all.bind('<Button>', lambda event: deselect_all_command(event))
        button_deselect_all.grid(column=1, row=6)

    # BUG: why does it need double click to show the list?
    def reset_file_list(self, folder_index=None):
        """updates the listbox with files from within the mod folder
        """
        if folder_index is not None:
            self.folder_index = folder_index

            self.listbox2.delete(0, END)
            print(f"{folder_index = }")
            pp(self.func_get_config(), indent=4)
            mod_folder_name = get_folder_names(self.func_get_config()['source_folder_path'])[folder_index]
            # print(os.path.join(self.func_get_config()['source_folder_path'], mod_folder_name))
            items_list = get_folder_contents(self.func_get_config()['source_folder_path'])[folder_index]['files']
            for item in items_list:
                self.listbox2.insert(END, item)
    

# BOOKMARK: LISTBOX 1


class ListBoxFrame1(Frame):
    def __init__(self, master, func_get_config, item_select_command, full_height=False):
        super().__init__(master)
        self.master = master

        self.func_get_config = func_get_config

        self.title_label = ttk.Label(
            self, text='Mod Folders', font=("TkDefaultFont", 12, "bold")
        )
        self.title_label.grid(column=0, columnspan=2, row=0)

        self.listbox1 = Listbox(self, selectmode="single")
        self.listbox1.bind('<<ListboxSelect>>', lambda event: item_select_command(event))
        self.populate_list()

        if full_height:
            self.listbox1.grid(
                column=0, columnspan=2, row=1, rowspan=5, sticky="n"
            )
        else:
            self.listbox1.grid(
                column=0, columnspan=2, row=1, rowspan=2
            ) 

    def populate_list(self, folder_path=None):
        print('called')
        if folder_path==None:
            subfolder_list = get_folder_names(self.func_get_config()['source_folder_path'])
        else:
            subfolder_list = get_folder_names(folder_path)
        self.listbox1.delete(0, END)
        for item in subfolder_list:
            self.listbox1.insert(END, item)


# MSG: Settings tab


class FolderPathEntry(Frame):
    def __init__(self, master, label_text, variable, browse_command, path_type):
        super().__init__(master)
        self.master = master

        self.path_type = path_type

        self.folder_label = ttk.Label(self, text=label_text)
        self.folder_label.grid(column=0, columnspan=2, row=0)

        self.folder_entry = ttk.Entry(
            self, 
            textvariable=variable, 
            width=25
        )  
        self.folder_entry.grid(column=2, columnspan=3, row=0, padx=15)

        self.browse_button = ttk.Button(
            self,
            text="Browse",
            style="Custom1.TButton",
            command=lambda: browse_command(variable, self.path_type),
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
        self.selected_mod_files = []

        # load config
        self.read_config()

        # initiate Tkinter
        self.root = Tk()
        self.root.title(self.app_title)
        self.root.geometry(self.app_window_size)
        self.root.resizable(False, False)

        # Load styles
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

        self.mod_options_frame = ButtonBar(
            self.manage_content_frame,
            self.refresh_mod_list
            )
        self.mod_options_frame.grid(column=6, row=0, rowspan=6)
        # TODO: under construction
        self.listbox_frame_2 = ListBoxFrame2(
            self.manage_content_frame, 
            self.read_config,
            self.handle_file_selection,
            self.handle_select_all,
            self.handle_deselect_all
        )
        self.listbox_frame_2.grid(column=2, columnspan=2, row=0, rowspan=6, sticky="n")

        self.listbox_frame_1 = ListBoxFrame1(
            self.manage_content_frame, 
            self.read_config,
            self.handle_folder_selection,
            full_height=True
        )
        self.listbox_frame_1.grid(column=0, columnspan=2, row=0, rowspan=6)

        # MSG: Settings tab layout

        self.source_folder_path_var = StringVar(value=self.app_config['source_folder_path'] if self.app_config['source_folder_path'] else None)
        self.source_folder_path_var.trace('w',lambda name, index, mode, sv=self.source_folder_path_var: self.handle_path_change(name, index, mode, sv, path_type='source'))
        self.source_folder_entry = FolderPathEntry(
            self.settings_frame,
            "Source Folder        ",
            self.source_folder_path_var,
            self.handle_browse,
            'source'
        )
        self.source_folder_entry.grid(column=0, columnspan=6, row=0)

        self.destination_folder_path_var = StringVar(value=self.app_config['destination_folder_path'] if self.app_config['destination_folder_path'] else None)
        self.destination_folder_path_var.trace('w',lambda name, index, mode, sv=self.destination_folder_path_var: self.handle_path_change(name, index, mode, sv, path_type='destination'))
        self.destination_folder_entry = FolderPathEntry(
            self.settings_frame,
            "Destination Folder",
            self.destination_folder_path_var,
            self.handle_browse,
            'destination'
        )
        self.destination_folder_entry.grid(column=1, columnspan=6, row=1)

        # Run the main loop
        self.root.mainloop()

    def handle_folder_selection(self, event):
        selected_index = event.widget.curselection()[0]
        selected_item = event.widget.get(selected_index)
        self.listbox_frame_2.reset_file_list(folder_index=selected_index)
        self.set_mod_folder_index(selected_index)
        self.clear_mod_file_indexes()
    
    def set_mod_folder_index(self, index):
        self.mod_folder_index = index
    
    def get_mod_folder_index(self):
        return self.mod_folder_index

    def clear_mod_folder_index(self):
        self.mod_folder_index = None
    
    def set_mod_files_indexes(self, indexes):
        self.selected_mod_files = indexes
    
    def get_mod_file_indexes(self):
        return self.selected_mod_files

    def clear_mod_file_indexes(self):
        self.selected_mod_files = []

    # TODO: make this maintain a list of selected files
    def handle_select_all(self, event, folder_index):
        print(folder_index)
        print(self.get_mod_file_indexes())
        print()
        if folder_index is not None:
            mod_files = get_folder_contents(self.read_config()['source_folder_path'])[folder_index]['files']
            self.selected_mod_files = mod_files

    def handle_deselect_all(self):
        pass

    def handle_file_selection(self, event):
        print(">> handle_file_selection")
        # print(event.widget.curselection())
        # selected_index = event.widget.curselection()[0]
        # selected_item = event.widget.get(selected_index)
        self.selected_mod_files = event.widget.curselection()
        print(self.selected_mod_files)

    def get_base_dir(self):
        return self.app_base_dir

    def handle_browse(self, data, path_type):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            if path_type == 'source':
                self.set_source_folder_path(selected_folder)
                self.source_folder_path_var.set(selected_folder)
            elif path_type == 'destination':
                self.set_destination_folder_path(selected_folder)
                self.destination_folder_path_var.set(selected_folder)

    def handle_path_change(self, name, index, mode, sv, path_type):
        if sv.get():
            if path_type == 'source':
                self.set_source_folder_path(sv.get())
                self.source_folder_path_var.set(sv.get())
                self.listbox_frame_1.populate_list(folder_path=sv.get())
            elif path_type == 'destination':
                self.set_destination_folder_path(sv.get())
                self.destination_folder_path_var.set(sv.get())

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
        with open(os.path.abspath(self.config_file_name), "w") as file:
            json.dump(config, file, indent=4)
    
    def refresh_mod_list(self, event):
        folder_contents = get_folder_contents(self.read_config()['source_folder_path'])
        folder_names = get_folder_names(self.read_config()['source_folder_path'])
        print(folder_contents)
        print(folder_names)

    def set_source_folder_path(self, path):
        if not os.path.isabs(path):
            raise ValueError('Path should be absolute not relative.')
        self.clear_mod_folder_index()
        self.write_config(
            'source_folder_path', 
            path
        )
        

    def set_destination_folder_path(self, path):
        if not os.path.isabs(path):
            raise ValueError('Path should be absolute not relative.')
        
        self.write_config(
            'destination_folder_path', 
            path
        )

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
    print('-------------------------starter-------------------------')
    mm = ModManager()
    print('-------------------------end-------------------------')

