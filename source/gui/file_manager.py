import tkinter as tk
from tkinter import ttk
from pathlib import Path
from source.dag.dag import DAG


class FileManagerWidget(tk.Frame):
    def __init__(self, master, project_name, **kwargs):
        super().__init__(master, width=600, background="#282c34", **kwargs)
        self.current_root = Path(Path.cwd(), project_name)
        self.dirs = None
        self.files = None
        self.new_name = None
        self.open_dirs_dict = None
        self.tree = None
        self.context_menu = None

        self.create_context_menu()
        self.create_widgets()
        self.icon = tk.PhotoImage(
            file=Path(Path.cwd(), "source", "gui", "icons", "folder_icon.png")
        )  # Add your actual image data here
        # Initialize the treeview with the root directory
        self.populate_treeview("", self.current_root)

    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="New", command=lambda: print("New File"))
        self.context_menu.add_command(
            label="Delete", command=lambda: print("deleting file")
        )
        self.context_menu.add_command(
            label="Paste", command=lambda: print("Paste file")
        )
        self.context_menu.add_command(label="Copy", command=lambda: print("Copy file"))
        self.context_menu.add_command(
            label="Copy Path", command=lambda: print("Copy Path")
        )
        self.context_menu.add_command(
            label="Rename", command=lambda: print("Rename File")
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Run Dag", command=lambda: print("Run Dag"))
        self.context_menu.add_command(
            label="Render Dag", command=self.render_dag_from_file
        )

    def show_context_menu(self, event):
        item_id = self.tree.identify_row(event.y)
        self.tree.selection_set(item_id)
        self.tree.focus(item_id)
        if item_id == "":
            return

        try:
            self.context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.context_menu.grab_release()

    def create_widgets(self):
        self.tree = ttk.Treeview(self)
        self.tree.heading("#0", text=str(self.current_root), anchor="w")
        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<Button-3>", self.show_context_menu)  # Bind right-click event

    def populate_treeview(self, parent, node):
        parent_id = parent if parent else ""
        path = Path(node)
        for item in path.iterdir():
            parameters = {
                "text": item.name,
                "values": (item.is_dir(), item.as_posix()),
            }
            if item.is_dir():
                parameters["image"] = self.icon

            item_id = self.tree.insert(parent_id, "end", **parameters)
            if item.is_dir():
                self.populate_treeview(item_id, item)

    def render_dag_from_file(self):
        item_id = self.tree.focus()

        dag_name = self.tree.item(item_id, "text")
        isdir = self.tree.item(item_id, "values")[0]

        if isdir == "True":
            return

        file_path = self.tree.item(item_id, "values")[1]

        dag = DAG.read_from_xml(file_path)

        self.master.master.add_tab(dag, dag_name)
