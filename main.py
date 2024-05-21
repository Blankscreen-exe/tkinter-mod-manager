from tkinter import Tk, ttk, filedialog
from tkinter import Listbox
from pprint import pprint as pp


# Sample items lists (replace with your data source)
items_lists = [[], []]
for index in range(20):
  items_lists[0].append(f'Item A - {index}')
  items_lists[1].append(f'Item B - {index}')

# Function to handle listbox selection (replace with your logic)
def handle_selection(event, listbox_index):
  selected_index = event.curselection[0]
  selected_item = items_lists[listbox_index][selected_index]
  pp(vars(event))
  print(f"Selected item in listbox {listbox_index}:", selected_item)

# Function to handle browse button click
def handle_browse(folder_path_var):
  selected_folder = filedialog.askdirectory()
  if selected_folder:
    folder_path_var.set(selected_folder)

# Create the main window
root = Tk()
root.title("Mod Manager")
root.geometry("450x220")  # Set initial window size
root.resizable(False, False)

# Create the notebook (tabs container)
notebook = ttk.Notebook(root)
# notebook.pack(expand=True, fill="both")
notebook.grid(column=0, columnspan=6, row=0, rowspan=6)

# Create frames for each tab
manage_frame = ttk.Frame(notebook)
settings_frame = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(manage_frame, text="Manage")
notebook.add(settings_frame, text="Settings")

# Manage tab layout

# Frame to hold both listboxes and buttons
manage_content_frame = ttk.Frame(manage_frame)
# manage_content_frame.pack(padx=10, pady=10)  # Add some padding
manage_content_frame.grid(column=0, columnspan=6, row=0, rowspan=6)

# BOOKMARK: BUTTON OPTIONS

# Left side frame for Listbox 2, title, and buttons
right_frame = ttk.Frame(manage_content_frame)
# right_frame.pack(side="right")
right_frame.grid(column=6, row=0, rowspan=6)

# Title label for Listbox 2 (bold)
# listbox2_title = ttk.Label(right_frame, text="Mod Files", font=("TkDefaultFont", 12, "bold"))
# listbox2_title.pack(padx=5, pady=5)

# Listbox 2
# listbox2 = Listbox(right_frame, height=5, selectmode="browse")
# for item in items_lists[1]:
#   listbox2.insert("end", item)
# listbox2.bind("<<ListboxSelect>>", lambda event: handle_selection(event, 1))  # Bind selection event
# listbox2.pack(fill="both", expand=True)

# button styles
button_style = ttk.Style().configure('W.TButton', font = ('calibri', 8, 'normal'))

# Buttons for Listbox 2 
button1 = ttk.Button(right_frame, text="Refresh List", style=button_style)
# button1.pack(side='top', fill='x')
button1.grid(column=6, row=2)
button1 = ttk.Button(right_frame, text="Install Mod", style=button_style)
# button1.pack(side='top', fill='x')
button1.grid(column=6, row=3)
button2 = ttk.Button(right_frame, text="Uninstall Mods", style=button_style)
# button2.pack(side='top', fill='x')
button2.grid(column=6, row=4)


# BOOKMARK: LISTBOX 2

# Left side frame for Listbox 2, title, and buttons
right_frame = ttk.Frame(manage_content_frame)
# right_frame.pack(side="right")
right_frame.grid(column=2, columnspan=2, row=0, rowspan=6)

# Title label for Listbox 2 (bold)
listbox2_title = ttk.Label(right_frame, text="Mod Files", font=("TkDefaultFont", 12, "bold"))
# listbox2_title.pack(padx=5, pady=5, side='top')
listbox2_title.grid(column=2, columnspan=2, row=0)

# Listbox 2
listbox2 = Listbox(right_frame, height=5, selectmode="browse")
for item in items_lists[1]:
  listbox2.insert("end", item)
listbox2.bind("<<ListboxSelect>>", lambda event: handle_selection(event, 1))  # Bind selection event
# listbox2.pack(fill="both", expand=True, side='top')
listbox2.grid(column=2, columnspan=2, row=1, rowspan=5, sticky='n')

# button styles
button_style = ttk.Style().configure('W.TButton', font = ('calibri', 8, 'normal'))

# Buttons for Listbox 2 
button1 = ttk.Button(right_frame, text="Select All", style=button_style)
# button1.pack(side='left')
button1.grid(column=2, row=6)
button2 = ttk.Button(right_frame, text="De-Select All", style=button_style)
# button2.pack(side='right')
button2.grid(column=3, row=6)

# BOOKMARK: LISTBOX 1

# Right side frame for Listbox 1 and title
left_frame = ttk.Frame(manage_content_frame)
# left_frame.pack(side="left", fill="both", expand=True)
left_frame.grid(column=0, columnspan=2, row=0, rowspan=6)

# Title label for Listbox 1 (bold)
listbox1_title = ttk.Label(left_frame, text="Mod List", font=("TkDefaultFont", 12, "bold"))
# listbox1_title.pack(padx=5, pady=5)
listbox1_title.grid(column=0, columnspan=2, row=0)

# Listbox 1 (full height)
listbox1 = Listbox(left_frame, selectmode="browse")
for item in items_lists[0]:
  listbox1.insert("end", item)
listbox1.bind("<<ListboxSelect>>", lambda event: handle_selection(event, 0))  # Bind selection event
# listbox1.pack(fill="y", expand=True, side='left')
listbox1.grid(column=0, columnspan=2, row=1, rowspan=2)

# REVIEW: ---------------------------------------------------

# Settings tab (remains the same as before)
# settings_label = ttk.Label(settings_frame, text="This is the Settings tab content.")
# # settings_label.pack(padx=10, pady=10)
# settings_label.grid(column=0, columnspan=6, row=0, rowspan=6)

# BOOKMARK: source folder

row_frame1 = ttk.Frame(settings_frame)
# row_frame1.pack(fill="x", pady=5)
row_frame1.grid(column=0, columnspan=6, row=0)

source_folder_path_var = ''

# Label for folder path
folder_label = ttk.Label(row_frame1, text='Source Folder        ')
# folder_label.pack(side="left")
folder_label.grid(column=0, columnspan=2, row=0)


# Input box for folder path
folder_entry = ttk.Entry(row_frame1, textvariable=source_folder_path_var, width=25)  # Adjust width as needed
# folder_entry.pack(side="left", expand=True)
folder_entry.grid(column=2, columnspan=3, row=0)


# Browse button
browse_button = ttk.Button(row_frame1, text="Browse", command=(lambda var=source_folder_path_var: handle_browse(var)))
# browse_button.pack(side="right")
browse_button.grid(column=6, row=0)


# BOOKMARK: destination folder

row_frame2 = ttk.Frame(settings_frame)
# row_frame2.pack(fill="x", pady=5)
row_frame2.grid(column=1, columnspan=6, row=1)

destination_folder_path_var = ''

# Label for folder path
folder_label = ttk.Label(row_frame2, text='Destination Folder')
# folder_label.pack(side="left")
folder_label.grid(column=0, columnspan=2, row=1)


# Input box for folder path
folder_entry = ttk.Entry(row_frame2, textvariable=destination_folder_path_var, width=25)  # Adjust width as needed
# folder_entry.pack(side="left", expand=True)
folder_entry.grid(column=2, columnspan=3, row=1)


# Browse button
browse_button = ttk.Button(row_frame2, text="Browse", command=(lambda var=destination_folder_path_var: handle_browse(var)))
# browse_button.pack(side="right")
browse_button.grid(column=6, row=1)


# Run the main loop
root.mainloop()

