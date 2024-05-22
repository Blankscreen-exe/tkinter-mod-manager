from tkinter import Tk, ttk, filedialog, Frame, StringVar
from tkinter import Listbox
from pprint import pprint as pp
from functions import *
import os

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
def handle_selection(event, listbox_type):
  selected_index = event.widget.curselection()[0]
  selected_item = event.widget.get(selected_index)
  mod_folder_path = os.path.join(config.source_folder)
  print(mod_folder_path)
  items_lists[1] = get_folder_contents(mod_folder_path)[selected_index]['files']
  print(items_lists[1])

  print(f"Selected item in listbox {listbox_type}: {selected_item} mit {selected_index}")

  # TODO: Update the target listbox based on the selection
  target_listbox.delete(0, tk.END)  # Clear target listbox first (optional)
  # Add new items to the target listbox based on selected item or logic
  target_listbox.insert("end", "New Item 1 based on", selected_item)
  target_listbox.insert("end", "New Item 2 based on", selected_item)


# Function to handle browse button click
def handle_browse(folder_path_var):
  selected_folder = filedialog.askdirectory()
  if selected_folder:
    folder_path_var.set(selected_folder)

# Create the main window
root = Tk()
root.title("Mod Manager")
root.geometry("440x220")  # Set initial window size
root.resizable(False, False)

button_style = ttk.Style()
button_style.configure(
            'Custom.TButton',
            font=('Calibri', 8, 'normal'),
            foreground='white',
            background='#278ef0',
            width='11',
        )
button_style.map('Custom.TButton',
    foreground=[('active', '!disabled', 'black')],
    background=[('active', '!disabled', '#a9d3fa')],
)

# Create the notebook (tabs container)
notebook = ttk.Notebook(root)
notebook.grid(column=0, columnspan=6, row=0, rowspan=6)

# Create frames for each tab
manage_frame = ttk.Frame(notebook)
settings_frame = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(manage_frame, text="Manage")
notebook.add(settings_frame, text="Settings")

# MSG: Manage tab layout

# Frame to hold both listboxes and buttons
manage_content_frame = ttk.Frame(manage_frame)
# manage_content_frame.pack(padx=10, pady=10)  # Add some padding
manage_content_frame.grid(column=0, columnspan=6, row=0, rowspan=6)

# BOOKMARK: scroll listbox

class ScrollableListbox(Frame):
    def __init__(self, master, items, width=50, height=10, selectmode="browse"):
        super().__init__(master)  # Call parent constructor
        self.master = master

        # Listbox
        self.listbox = Listbox(self, selectmode=selectmode, width=width, height=height)
        for item in items:
            self.listbox.insert("end", item)
        self.listbox.grid(column=0,row=0)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(column=1,row=0)

        # Link scrollbar and listbox
        self.listbox.config(yscrollcommand=self.scrollbar.set)

# BOOKMARK: BUTTON OPTIONS

class ButtonBar(Frame):
    def __init__(self, master, button_texts=["Refresh List", "Install Mod", "Uninstall Mods"]):
        super().__init__(master)  # Call parent constructor
        self.master = master

        button = ttk.Button(self, text=' Refresh List ', style="Custom.TButton")
        button.grid(column=0, row=0, sticky='n', padx=3)  
        button = ttk.Button(self, text='  Install Mod  ', style="Custom.TButton")
        button.grid(column=0, row=1, sticky='n', padx=3)  
        button = ttk.Button(self, text='Uninstall Mod', style="Custom.TButton")
        button.grid(column=0, row=2, sticky='n', padx=3)  


# BOOKMARK: LISTBOX 2

class ListBoxFrame2(Frame):
    def __init__(self, master, title_text, items_list):
        super().__init__(master)  # Call parent constructor
        self.master = master

        # Create title label
        self.title_label = ttk.Label(self, text=title_text, font=("TkDefaultFont", 12, "bold"))
        self.title_label.grid(column=0, columnspan=2, row=0)

        # Create listbox
        self.listbox2 = Listbox(self, height=5, selectmode="multiple")
        for item in items_list:
            self.listbox2.insert("end", item)
        self.listbox2.bind("<<ListboxSelect>>", lambda event: handle_selection(event, 'mod-file-list'))
        self.listbox2.grid(column=0, columnspan=2, row=1, rowspan=5, ipadx=7)

        # Create buttons dynamically
        button_texts = ["Select All", "De-Select All"]
        for i, text in enumerate(button_texts):
            button = ttk.Button(self, text=text, style="Custom.TButton")
            button.grid(column=i, row=6)  # Adjust grid options

# BOOKMARK: LISTBOX 1

class ListBoxFrame1(Frame):
    def __init__(self, master, title_text, items_list, full_height=False):
        super().__init__(master)  # Call parent constructor
        self.master = master

        # Create title label
        self.title_label = ttk.Label(self, text=title_text, font=("TkDefaultFont", 12, "bold"))
        self.title_label.grid(column=0, columnspan=2, row=0)

        # Create listbox
        self.listbox1 = Listbox(self, selectmode="browse")
        for item in items_list:
            self.listbox1.insert("end", item)
        self.listbox1.bind("<<ListboxSelect>>", lambda event: handle_selection(event, "mod-folder-list"))
        if full_height:
            self.listbox1.grid(column=0, columnspan=2, row=1, rowspan=5, sticky='n')  # Adjust for full height
        else:
            self.listbox1.grid(column=0, columnspan=2, row=1, rowspan=2)  # Adjust for partial height


# MSG: Settings tab

class FolderPathEntry(Frame):
    def __init__(self, master, label_text, variable, browse_command):
        super().__init__(master)  # Call parent constructor
        self.master = master

        # Label for folder path
        self.folder_label = ttk.Label(self, text=label_text)
        self.folder_label.grid(column=0, columnspan=2, row=0)

        # Input box for folder path
        self.folder_entry = ttk.Entry(self, textvariable=variable, width=25)  # Adjust width as needed
        self.folder_entry.grid(column=2, columnspan=3, row=0, padx=15)

        # Browse button
        self.browse_button = ttk.Button(self, text="Browse", style='Custom.TButton', command=lambda: browse_command(variable))
        self.browse_button.grid(column=6, row=0)


# -----------------------------------------------------------------
right_frame = ButtonBar(manage_content_frame, ["Refresh List", "Install Mod", "Uninstall Mods"])
right_frame.grid(column=6, row=0, rowspan=6)

listbox_frame_2 = ListBoxFrame2(manage_content_frame, "Mod Files", items_lists[1])
listbox_frame_2.bind('<Button>' ,handle_selection)
listbox_frame_2.grid(column=2, columnspan=2, row=0, rowspan=6, sticky='n')

listbox_frame_1 = ListBoxFrame1(manage_content_frame, "Mod List", items_lists[0], full_height=True)
listbox_frame_1.bind('<Button>' ,handle_selection)
listbox_frame_1.grid(column=0, columnspan=2, row=0, rowspan=6)

# Example usage (Source folder)
source_folder_path_var = StringVar()
source_folder_entry = FolderPathEntry(settings_frame, "Source Folder        ", source_folder_path_var, handle_browse)
source_folder_entry.grid(column=0, columnspan=6, row=0)

# Example usage (Destination folder)
destination_folder_path_var = StringVar()
destination_folder_entry = FolderPathEntry(settings_frame, "Destination Folder", destination_folder_path_var, handle_browse)
destination_folder_entry.grid(column=1, columnspan=6, row=1)

# Run the main loop
root.mainloop()

