import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from folder_operator import AIFolderOperator
import os

class FolderOrganizerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Folder Organizer")
        self.master.geometry("700x400")

        self.folder_count = tk.IntVar(value=1)
        self.folders = []
        self.target_folder = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.organization_method = tk.StringVar(value="Filetype")
        self.auto_name_folders = tk.BooleanVar(value=False)
        self.min_items_per_folder = tk.IntVar(value=1)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Target folder selection
        ttk.Label(main_frame, text="Target Folder:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(main_frame, textvariable=self.target_folder, state="readonly", width=70).grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        ttk.Button(main_frame, text="Browse", command=self.select_target_folder).grid(row=0, column=3, padx=5, pady=5)

        # Organization method selection
        ttk.Label(main_frame, text="Organization Method:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(main_frame, textvariable=self.organization_method, values=["Filetype", "Date", "Filesize"], state="readonly").grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.organization_method.trace_add('write', self.on_method_change)

        # Auto-name folders checkbox
        ttk.Checkbutton(main_frame, text="Auto-name folders", variable=self.auto_name_folders, command=self.toggle_auto_name).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Minimum items per folder
        self.min_items_label = ttk.Label(main_frame, text="Minimum items per folder:")
        self.min_items_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.min_items_spinbox = ttk.Spinbox(main_frame, from_=1, to=10, textvariable=self.min_items_per_folder, width=5)
        self.min_items_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Number of sub-folders
        self.subfolder_label = ttk.Label(main_frame, text="Number of sub-folders:")
        self.subfolder_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.subfolder_spinbox = ttk.Spinbox(main_frame, from_=1, to=10, textvariable=self.folder_count, command=self.update_folder_inputs, width=5)
        self.subfolder_spinbox.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Folder frame
        self.folder_frame = ttk.Frame(main_frame)
        self.folder_frame.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Organize button
        ttk.Button(main_frame, text="Organize Files", command=self.organize_files).grid(row=6, column=0, columnspan=4, padx=5, pady=20)

        # Configure grid
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)

        self.update_folder_inputs()
        self.toggle_auto_name()

    def select_target_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.target_folder.set(folder_selected)

    def update_folder_inputs(self):
        for widget in self.folder_frame.winfo_children():
            widget.destroy()

        self.folders = []
        for i in range(self.folder_count.get()):
            ttk.Label(self.folder_frame, text=f"Folder {i+1} name:").grid(row=i, column=0, padx=5, pady=2, sticky="w")
            folder_entry = ttk.Entry(self.folder_frame, width=30)
            folder_entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            self.folders.append(folder_entry)

    def toggle_auto_name(self):
        if self.auto_name_folders.get():
            self.subfolder_label.grid_remove()
            self.subfolder_spinbox.grid_remove()
            self.folder_frame.grid_remove()
            self.min_items_label.grid()
            self.min_items_spinbox.grid()
        else:
            self.subfolder_label.grid()
            self.subfolder_spinbox.grid()
            self.folder_frame.grid()
            self.min_items_label.grid_remove()
            self.min_items_spinbox.grid_remove()

    def on_method_change(self, *args):
        if self.auto_name_folders.get():
            self.auto_name_folders.set(False)
            self.toggle_auto_name()

    def organize_files(self):
        if self.auto_name_folders.get():
            ai_operator = AIFolderOperator(self.target_folder.get(), [], self.organization_method.get(), self.min_items_per_folder.get())
            folder_names = ai_operator.get_auto_folder_names()
        else:
            folder_names = [folder.get() for folder in self.folders if folder.get()]
            if not folder_names:
                messagebox.showerror("Error", "Please enter at least one folder name.")
                return
            ai_operator = AIFolderOperator(self.target_folder.get(), folder_names, self.organization_method.get())

        ai_operator.run()
        messagebox.showinfo("Success", "Files organized successfully!")

def run_gui():
    root = tk.Tk()
    FolderOrganizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
