import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from source.gui.style import DynamicStyle, DynamicWidgetStyles
import numpy as np


class NodeWidget(tk.Frame):
    def __init__(
        self,
        master,
        id,
        name,
        operation,
        location,
        dynamic_style: DynamicStyle,
        **kwargs,
    ):

        super().__init__(
            master=master,
            **dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET),
            **kwargs,
        )
        self.dag_editor = master

        # Id
        self.id = id

        # set color
        self.color = tk.StringVar(
            self, dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET, "background")
        )
        self.configure(background=self.color.get())

        # Name/Operation/Location varibles
        self.name = tk.StringVar(value=name)
        self.operation = tk.StringVar(value=operation)
        self.location = tk.StringVar(value=location)

        # set the style
        self.dynamic_style = dynamic_style

        # save coordinates of frame
        self.start_x = None
        self.start_y = None

        # widgets
        self.entry_widgets = None
        self.label_widgets = None
        self.id_label = None

        # configure grid
        self.columnconfigure((0, 1, 2, 3), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="a")

        # edges attached
        self.edges = set()

        # bind actions to the frame
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", lambda _: self.config(cursor="arrow"))

        # Add Menu
        self.menu_button = None
        self.add_menu()

        # Add Entry Widgets
        self.add_widgets()

        #
        self.grid_propagate(False)

    def zoom(self, delta):
        self.config(width=self.winfo_width() + np.sign(delta) * 20,
                        height=self.winfo_height() +np.sign(delta) * 20)

        # change id label
        font = self.id_label.cget("font")
        height = self.id_label.cget("height")
        new_font = (font[0], font[1] + np.sign(delta))
        new_height = height + np.sign(delta)
        self.id_label.configure(font=new_font, height=new_height)

        # change labels
        for label in self.label_widgets:
            label.configure(**self.dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET_LABEL))

        # change entries
        for entry in self.entry_widgets:
            entry.configure(**self.dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET_ENTRY))


        self.menu_button.configure(**self.dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET_MENU_BUTTON))


    def on_press(self, event):
        self.config(cursor="hand2")
        self.start_x = event.x
        self.start_y = event.y
        self.lift()

    def on_drag(self, event):
        x = self.winfo_x() + (event.x - self.start_x)
        y = self.winfo_y() + (event.y - self.start_y)

        height, width = self.winfo_height(), self.winfo_width()

        # update the coordinates for the nodes
        self.place(x=x, y=y)

        # update the coordinates for the children edges
        for children_edge in self.master.children_edges[self.id]:
            line_coordinates = self.master.canvas.coords(children_edge)
            line_coordinates[0] = x + int(width / 2)
            line_coordinates[1] = y + height
            self.master.canvas.coords(children_edge, *line_coordinates)

        # update the coordinates for the parent edges
        for parent_edge in self.master.parent_edges[self.id]:
            line_coordinates = self.master.canvas.coords(parent_edge)
            line_coordinates[2] = x + int(width / 2)
            line_coordinates[3] = y
            self.master.canvas.coords(parent_edge, *line_coordinates)

        self.place(x=x, y=y)

    def add_menu(self):
        # menu button
        self.menu_button = NodeMenuButton(
            self,
            self.dynamic_style,
            **self.dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET_MENU_BUTTON)
        )
        self.menu_button.grid(
            row=0, column=3, columnspan=1, padx=10, pady=0, sticky="nsew"
        )

    def add_widgets(self):
        # adding Id label
        self.id_label = ctk.CTkLabel(
            self,
            text=f"Id: {self.id}",
            **self.dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET_ID)
        )
        self.id_label.grid(
            row=0, column=0, columnspan=8, padx=10, sticky=tk.W, pady=0
        )

        # Adding name/Operation/Location widgets
        text_strings = ["Name", "Operation", "Location"]

        name_entry = ctk.CTkEntry(
            self, textvariable=self.name, **self.dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET_LABEL)
        )
        operation_entry = ctk.CTkEntry(
            self, textvariable=self.operation, **self.dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET_LABEL)
        )
        location_entry = ctk.CTkEntry(
            self, textvariable=self.location, **self.dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET_LABEL)
        )

        self.entry_widgets = [name_entry, operation_entry, location_entry]
        self.label_widgets = []

        for index in range(len(text_strings)):
            self.label_widgets.append(
                ctk.CTkLabel(self, text=text_strings[index],
                             **self.dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET_LABEL))
            )
            self.label_widgets[index].grid(
                row=1 + 2 * index, column=0, columnspan=8, padx=10, sticky=tk.W, pady=0
            )

            self.entry_widgets[index].grid(
                row=2 + 2 * index, column=0, columnspan=8, padx=10, pady=0,sticky="nsew"
            )

    def change_color(self, color):
        self.configure(background=color)
        self.menu_button.color = color


class NodeMenuButton(tk.Label):
    def __init__(self,
                 master,
                 dynamic_style: DynamicStyle,
                 **kwargs):
        super().__init__(
            master,
            **kwargs,
        )
        self.color = "#3C3F41"
        self.node = master

        # set dynamic style
        self.dynamic_style = dynamic_style

        # Dropdown menu (hidden initially)
        self.menu_frame = tk.Frame(
            self.master.master,
            bd=1,
            background="#3C3F41",
            highlightbackground="grey",
            highlightthickness=1,
        )
        self.menu_visible = False

        self.bind("<Button-1>", self.clicked_button)

    def clicked_button(self, event):
        self.show_menu()
        self.config(background="#4b6eaf")

    def show_menu(self):
        if self.menu_visible:
            return

        self.menu_frame.place(
            x=self.master.winfo_x() + self.winfo_x(),
            y=self.master.winfo_y() + self.winfo_height() + self.winfo_y() - 1,
        )

        # configure grid
        self.rowconfigure((0, 1, 2, 3), weight=1)

        self.menu_frame.lift()

        options = ["Add Child Node", "Add Parent Node", "Add Edge", "Change Color"]
        self.labels = []

        # Create label widgets for each option and bind the selection
        for option_index in range(len(options)):
            label = MenuItem(
                self.menu_frame,
                node=self.node,
                text=options[option_index],
                **self.dynamic_style.get_style(DynamicWidgetStyles.NODE_WIDGET_MENU_ITEM)
            )
            label.grid(row=option_index, sticky=tk.W)
            self.labels.append(label)

        self.menu_visible = True
        self._root().bind("<Button-1>", self.hide_menu)

    def hide_menu(self, event):
        if not self.menu_visible:
            return

        if event.widget == self:
            return

        self.menu_frame.place_forget()
        for button in self.labels:
            button.pack_forget()
        self.menu_visible = False
        self.config(background=self.color)

    @staticmethod
    def menu_action(option):
        print(f"Selected: {option}")
        # Add your action for the selected menu option here


class MenuItem(tk.Label):
    def __init__(self, master, node, text, font,**kwargs):
        super().__init__(
            master,
            text=text,
            **kwargs
        )
        self.node = node
        self.command = text
        self.commands = {
            "Add Child Node": self.add_child_node,
            "Add Parent Node": self.add_parent_node,
            "Change Color": self.change_color,
        }

        self.bind("<Button-1>", self.run_menu_command)
        self.bind("<Button-3>", self.run_menu_command)
        self.bind("<Enter>", lambda event: self.config(background="#4b6eaf"))
        self.bind("<Leave>", lambda event: self.config(background="#3C3F41"))

    def run_menu_command(self, _):
        self.commands[self.command]()

    def add_child_node(self):
        x = self.master.winfo_x() - self.winfo_width()
        y = self.master.winfo_y() + 150

        new_child_node_id = self.node.dag_editor.get_new_node_id()

        self.node.dag_editor.dag.add_edge(self.node.id, new_child_node_id, 1)
        self.node.dag_editor.add_node(x, y, new_child_node_id, "new", "new", "old")
        self.node.dag_editor.add_edge(self.node.id, new_child_node_id)

    def add_parent_node(self):
        x = max(self.master.winfo_x() - self.winfo_width() + 50, 0)
        y = max(self.master.winfo_y() - self.winfo_height() - 200, 0)

        new_parent_node_id = self.node.dag_editor.get_new_node_id()

        self.node.dag_editor.dag.add_edge(new_parent_node_id, self.node.id, 1)
        self.node.dag_editor.add_node(x, y, new_parent_node_id, "new", "new", "old")
        self.node.dag_editor.add_edge(new_parent_node_id, self.node.id)

    def change_color(self):
        self.node.change_color("blue")