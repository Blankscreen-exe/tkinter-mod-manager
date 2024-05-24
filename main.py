from tkinter import Tk, ttk, filedialog, Frame, StringVar, IntVar, Variable, END, PhotoImage
from tkinter import Listbox
from functions import *
import os
import json
import platform
import logging

logging.basicConfig(filename='app.log', filemode='a', level=logging.DEBUG, format="[%(asctime)s](%(name)s - %(levelname)s): %(message)s")
logging.info('This will get logged to a file', exc_info=True)

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
        super().__init__(master)
        self.master = master

        self.func_get_config = func_get_config

        self.title_label = ttk.Label(
            self, text='Mod Files', font=("TkDefaultFont", 12, "bold")
        )
        self.title_label.grid(column=0, columnspan=2, row=0)

        self.listbox2 = Listbox(self, height=5, selectmode="multiple")

        self.listbox2.bind(
            "<<ListboxSelect>>", lambda event: item_select_command(event)
        )
        self.listbox2.grid(column=0, columnspan=2, row=1, rowspan=5, ipadx=7)
        
        button_select_all = ttk.Button(self, text="Select All", style="Custom1.TButton")
        button_select_all.bind('<Button>', lambda event: select_all_command(event, self.folder_index))
        button_select_all.grid(column=0, row=6)
        button_deselect_all = ttk.Button(self, text="De-Select All", style="Custom1.TButton")
        button_deselect_all.bind('<Button>', lambda event: deselect_all_command())
        button_deselect_all.grid(column=1, row=6)

    def reset_file_list(self, folder_index=None, selected_indexes=[]):
        """updates the listbox with files from within the mod folder
        """
        try:
            if folder_index is not None:
                self.folder_index = folder_index
                self.listbox2.delete(0, END)
                items_list = get_folder_contents(self.func_get_config()['source_folder_path'])[folder_index]['files']
                for ind, item in enumerate(items_list):
                    if ind in selected_indexes:
                        self.listbox2.insert(END, "➕ "+item)
                    else:
                        self.listbox2.insert(END, item)
                for index in selected_indexes:
                    self.listbox2.selection_set(index)
        except Exception as e:
            logging.exception(e)
    

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

    def populate_list(self, selected_folder_index=None):
        config = self.func_get_config()
        
        subfolder_list = get_folder_names(config['source_folder_path'])

        self.listbox1.delete(0, END)
        for ind, item in enumerate(subfolder_list):
            if ind == selected_folder_index:
                self.listbox1.insert(END, "➜ "+item)
            else:
                self.listbox1.insert(END, item)
        if selected_folder_index:
            self.listbox1.selection_set(selected_folder_index)

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
        self.app_window_size = "365x220" if platform.system() == "Windows" else "440x220" 
        self.config_file_name = 'modmanager_config.json'
        self.app_icon = '.\\shape.png'
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
        # cannot be used with pyinstaller
        # self.app_icon = PhotoImage(file=os.path.abspath(self.app_icon))
        self.app_icon = PhotoImage(file=self.app_icon)
        self.root.iconphoto(True, self.app_icon)
        # self.root.iconbitmap(os.path.abspath(self.app_icon))

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
            self.refresh_mod_list,
            self.install_mods,
            self.uninstall_mods
            )
        self.mod_options_frame.grid(column=6, row=0, rowspan=6)

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
        try:
            self.listbox_frame_1.populate_list(selected_folder_index=selected_index)

            self.clear_mod_file_indexes()
            self.listbox_frame_2.reset_file_list(folder_index=selected_index, selected_indexes=self.get_mod_file_indexes())
            self.set_mod_folder_index(selected_index)
        except Exception as e:
            logging.exception(e)
    
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

    def handle_select_all(self, event, folder_index):
        try:
            if folder_index is not None:
                mod_files = [ind for ind, _ in enumerate(get_folder_contents(self.read_config()['source_folder_path'])[folder_index]['files'])]
                self.set_mod_files_indexes(mod_files)
            
            self.listbox_frame_2.reset_file_list(folder_index=folder_index, selected_indexes=self.get_mod_file_indexes())
        except Exception as e:
            logging.exception(e)

    def handle_deselect_all(self):
        try:
            self.clear_mod_file_indexes()
            folder_index = self.listbox_frame_2.folder_index
            self.listbox_frame_2.reset_file_list(folder_index=folder_index, selected_indexes=self.get_mod_file_indexes())
        except Exception as e:
            logging.exception(e)

    def handle_file_selection(self, event):
        try:
            selected_index = self.listbox_frame_2.folder_index
            self.set_mod_files_indexes(event.widget.curselection())
            self.listbox_frame_2.reset_file_list(folder_index=selected_index, selected_indexes=self.selected_mod_files)
        except Exception as e:
            logging.exception(e)

    def handle_browse(self, data, path_type):
        selected_folder = filedialog.askdirectory()
        try:
            if selected_folder:
                if path_type == 'source':
                    self.set_source_folder_path(selected_folder)
                    self.source_folder_path_var.set(selected_folder)
                elif path_type == 'destination':
                    self.set_destination_folder_path(selected_folder)
                    self.destination_folder_path_var.set(selected_folder)
        except Exception as e:
            logging.exception(e)

    def handle_path_change(self, name, index, mode, sv, path_type):
        config = self.read_config()
        try:
            if sv.get():
                if path_type == 'source':
                    self.set_source_folder_path(sv.get())
                    self.source_folder_path_var.set(sv.get())
                    self.listbox_frame_1.populate_list()
                elif path_type == 'destination':
                    self.set_destination_folder_path(sv.get())
                    self.destination_folder_path_var.set(sv.get())
        except Exception as e:
            logging.exception(e)

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
        try:
            folder_contents = get_folder_contents(self.read_config()['source_folder_path'])
            folder_names = get_folder_names(self.read_config()['source_folder_path'])
            self.listbox_frame_1.populate_list()
        except Exception as e:
            logging.exception(e)

    def set_source_folder_path(self, path):
        try:
            if not os.path.isabs(path):
                raise ValueError('Path should be absolute not relative.')
            self.clear_mod_folder_index()
            self.write_config(
                'source_folder_path', 
                path
            )
        except Exception as e:
            logging.exception(e)
        

    def set_destination_folder_path(self, path):
        try:
            if not os.path.isabs(path):
                raise ValueError('Path should be absolute not relative.')
            
            self.write_config(
                'destination_folder_path', 
                path
            )
        except Exception as e:
            logging.exception(e)

    def get_config_template(self):
        return {
            "source_folder_path": "",
            "destination_folder_path": "",
            # REVIEW: not using it anymore, fetching file list from the functions instead
            # "mod_list": [
                # REF: Example mod list item
                # {
                #   "folder_name": "",
                #   "files": []
                # }
            # ],
        }

    def install_mods(self, folder_name):
        try:
            s = self.read_config()
            mod_folder_index = self.get_mod_folder_index()

            mod_folder_name = get_folder_names(s['source_folder_path'])[mod_folder_index]
            src_dir = os.path.join( s['source_folder_path'], mod_folder_name)
            all_file_names = get_folder_contents(s['source_folder_path'])[mod_folder_index]['files']
            filtered_file_list =  [file_name for ind, file_name in enumerate(all_file_names) if ind in self.get_mod_file_indexes()]
            dst_dir = s['destination_folder_path']
            copy_files(src_dir, filtered_file_list, dst_dir)
        except Exception as e:
            logging.exception(e)

    def uninstall_mods(self, folder_name):
        try:
            s = self.read_config()
            mod_folder_index = self.get_mod_folder_index()
            mod_folder_name = get_folder_names(s['source_folder_path'])[mod_folder_index]
            src_dir = os.path.join( s['source_folder_path'], mod_folder_name)
            all_file_names = get_folder_contents(s['source_folder_path'])[mod_folder_index]['files']
            filtered_file_list =  [file_name for ind, file_name in enumerate(all_file_names) if ind in self.get_mod_file_indexes()]
            dst_dir = s['destination_folder_path']
            delete_files(filtered_file_list, dst_dir)
        except Exception as e:
            logging.exception(e)

    def get_styles(self):
        button_style = ttk.Style()
        button_style.configure(
            "Custom1.TButton",
            font=("Calibri", 8, "normal"),
            foreground="black" if self.os_is_windows else "white",
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

