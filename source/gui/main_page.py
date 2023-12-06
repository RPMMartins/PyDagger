import tkinter as tk
from source.gui.file_manager import FileManagerWidget
from source.gui.menu_bar import MenuBar
import customtkinter as ctk
from source.gui.DagEditor import DagEditor
from source.gui.style import StaticStyle, DynamicStyle
from tkinter import ttk


class MainPage(ctk.CTk):
    def __init__(self, project_name, width_percent=0.7, height_percent=0.7, **kwargs):
        super().__init__(**kwargs)

        self.panedwin = None
        self.dag_editor_frame = None
        self.file_manager_frame = None
        self.tabControl = None

        self.width_percent = width_percent
        self.height_percent = height_percent

        self.project_name = project_name

        # set title and window size
        self.title(f"PyDagger - {self.project_name}")
        self.set_window_size()

        # set static style
        self.static_style = StaticStyle()
        self.dynamic_style = DynamicStyle()

        # set menu bar with widgets
        self.menu_bar = MenuBar(self, static_style=self.static_style)

        # set window panels with file manager and dag editors
        self.set_window_panel()

        self.iconbitmap("C:\\Users\\ruime\\Downloads\\purepng.com-black-dogdog-pet-animal-black-981524653986ga57n-min"
                       ".ico")

    def set_window_panel(self):
        self.panedwin = tk.PanedWindow(self, orient="horizontal", bd=0, bg="#3C3F41")
        self.panedwin.pack(fill="both", expand=True, padx=3)

    def set_file_manager(self):
        self.file_manager_frame = FileManagerWidget(self.panedwin, self.project_name)
        self.panedwin.add(self.file_manager_frame)

    def set_window_size(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = int(screen_width * self.width_percent)
        height = int(screen_height * self.height_percent)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

    def set_dag_editor(self):
        self.tabControl = ctk.CTkTabview(self, anchor="nw")

        self.panedwin.add(self.tabControl)

    def add_tab(self, dag, dag_name):
        if dag_name in self.tabControl._tab_dict.keys():
            return

        self.tabControl.add(dag_name)
        dag_editor_frame = DagEditor(
            self.tabControl.tab(dag_name),
            dag,
            self.project_name,
            self.static_style,
            self.dynamic_style
        )
        dag_editor_frame.pack(fill="both", expand=True)
        dag_editor_frame.render_dag()
