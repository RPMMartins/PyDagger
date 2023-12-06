import tkinter as tk
from source.gui.style import StaticStyle, StaticWidgetStyles


class MenuBar(tk.Frame):
    def __init__(self, master, static_style: StaticStyle, **kwargs):
        super().__init__(
            master, **static_style.get_style(StaticWidgetStyles.MENU_BAR), **kwargs
        )
        self.static_style = static_style

        # set the widgets
        self.set_widgets()

        self.pack(side=tk.TOP, fill=tk.X)

        # set the border frame
        self.set_border_frame()

        self.file_menu = None
        self.edit_menu = None

    def set_border_frame(self):
        border_frame = BottomBorderMenuBar(self.master, static_style=self.static_style)
        border_frame.pack(fill="both")

    def set_widgets(self):
        # buffer frame
        tk.Frame(self, width=10, bg=self.cget("bg")).pack(side=tk.LEFT, pady=2)

        # add file and edit menus
        self.file_menu = FileMenuButton(self, text="File", static_style =self.static_style)
        self.edit_menu = EditMenuButton(self, text="Edit", static_style =self.static_style)


class MenuButton(tk.Label):
    def __init__(self, master, text, static_style: StaticStyle):
        super().__init__(
            master,
            text=text,
            **static_style.get_style(StaticWidgetStyles.MENU_BAR_BUTTON)
        )
        self.static_style = static_style
        self.pack(side=tk.LEFT)

        # Dropdown menu (hidden initially)
        self.menu_frame = tk.Frame(self.master.master, bd=1, background="grey")
        self.menu_visible = False

        self.bind("<Button-1>", self.clicked_button)
        self.bind("<Button-3>", self.clicked_button)

        self.options = None

    def clicked_button(self, event):
        self.show_menu()
        self.config(background="#4b6eaf")

    def show_menu(self):
        if self.menu_visible:
            return
        self.menu_frame.place(
            x=self.master.winfo_x() + self.winfo_x(),
            y=self.master.winfo_y() + self.winfo_height() + self.winfo_y(),
        )
        self.menu_frame.lift()
        self.labels = []

        # Create label widgets for each option and bind the selection
        for option in self.options:
            label = MenuItem(self.menu_frame, self, text=option, static_style =self.static_style)

            self.labels.append(label)

        self.menu_visible = True
        self.master.master.bind("<Button-1>", self.hide_menu)
        self.master.master.bind("<Button-3>", self.hide_menu)

    def hide_menu(self, event):
        if not self.menu_visible:
            return

        if event.widget == self:
            return

        self.menu_frame.place_forget()
        for button in self.labels:
            button.pack_forget()
        self.menu_visible = False
        self.config(background="#3C3F41")

    @staticmethod
    def menu_action(option):
        print(f"Selected: {option}")
        # Add your action for the selected menu option here


class FileMenuButton(MenuButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.options = ["New Dag", "Open Dag", "Save As...", "Rename Project"]


class EditMenuButton(MenuButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.options = ["Undo", "Copy", "Paste", "Delete"]


class MenuItem(tk.Label):
    def __init__(self, master, menu_button, text,  static_style: StaticStyle):
        super().__init__(
            master,
            text=text,
            **static_style.get_style(StaticWidgetStyles.MENU_BAR_ITEM)
        )
        self.menu_button = menu_button

        self.pack(fill="x")
        self.bind("<Button-1>", lambda event: print(text))
        self.bind("<Button-3>", lambda event: print(text))
        self.bind("<Enter>", lambda event: self.config(background="#4b6eaf"))
        self.bind("<Leave>", lambda event: self.config(background="#3C3F41"))


class BottomBorderMenuBar(tk.Frame):
    def __init__(self, master,static_style: StaticStyle, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # Create a Canvas widget for drawing the border
        self.border_canvas = tk.Canvas(
            self, **static_style.get_style(StaticWidgetStyles.MENU_BAR_BORDER_CANVAS)
        )
        self.border_canvas.pack(fill="x")
