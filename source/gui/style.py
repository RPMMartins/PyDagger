from tkinter import ttk
from enum import Enum


class StaticWidgetStyles(str, Enum):
    TREEVIEW_HEADING = "Treeview.Heading"
    TREEVIEW = "Treeview"
    MENU_BAR = "menu_bar"
    MENU_BAR_BORDER_CANVAS = "menu_bar_border_canvas"
    MENU_BAR_BUTTON = "menu_bar_button"
    MENU_BAR_BUTTON_CLICKED = "menu_bar_button_clicked"
    MENU_BAR_FRAME = "menu_bar_frame"
    MENU_BAR_ITEM = "menu_bar_item"
    MENU_BAR_ITEM_ENTER = "menu_bar_item_enter"


class StaticStyle(ttk.Style):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set style
        self.theme_use("classic")

        # styles dictionary
        self.styles_dictionary = {}

        # set style for treeview
        self._set_treview_style()

        # Set styles for the menu bar
        self._set_menu_bar_style()

    def _set_treview_style(self):
        font = ("Fedora", 9, "")

        self.configure(
            "Treeview.Heading",
            font=font,
            background="#3C3F41",
            foreground="#d3d3d3",
            highlightthickness=0,
            padding=(5, 5),
            relief="flat",
        )

        self.map("Treeview.Heading", background=[("active", "")])

        self.configure(
            "Treeview",
            font=font,
            background="#3C3F41",
            fieldbackground="#3C3F41",
            foreground="#d3d3d3",
            padding=(5, 5),
            rowheight=30,
        )
        self.map(
            "Treeview",
            background=[("selected", "#4b6eaf")],
            foreground=[("selected", "#d3d3d3")],
        )

    def _set_menu_bar_style(self):
        self.styles_dictionary[StaticWidgetStyles.MENU_BAR] = {
            "bg": "#3C3F41",
        }

        self.styles_dictionary[StaticWidgetStyles.MENU_BAR_BORDER_CANVAS] = {
            "height": 1,
            "bd": 0,
            "highlightthickness": 0,
            "background": "grey",
        }

        self.styles_dictionary[StaticWidgetStyles.MENU_BAR_BUTTON] = {
            "padx": 5,
            "background": "#3C3F41",
            "foreground": "#d3d3d3",
            "pady": 5,
            "font": ("Fedora", 9, ""),
        }

        self.styles_dictionary[StaticWidgetStyles.MENU_BAR_BUTTON_CLICKED] = {
            "background": "#4b6eaf"
        }

        self.styles_dictionary[StaticWidgetStyles.MENU_BAR_FRAME] = {"background": "#grey"}

        self.styles_dictionary[StaticWidgetStyles.MENU_BAR_ITEM] = {
            "padx": 10,
            "background": "#3C3F41",
            "foreground": "#d3d3d3",
            "pady": 2,
            "font": ("Fedora", 9, ""),
        }

        self.styles_dictionary[StaticWidgetStyles.MENU_BAR_ITEM_ENTER] = {
            "background": "#4b6eaf",
        }

    def _set_panded_window_style(self):
        self.paned_window_color = "#3C3F41"
        self.paned_window_color_orientation = "horizontal"

    def get_style(self, widget_key: StaticWidgetStyles, key=None):
        if key is not None:
            return self.styles_dictionary[widget_key][key]
        return self.styles_dictionary[widget_key]


class DynamicWidgetStyles(str, Enum):
    NODE_WIDGET = "node_widget"
    NODE_WIDGET_ID = "node_widget_id"
    NODE_WIDGET_LABEL = "node_widget_label"
    NODE_WIDGET_ENTRY = "node_widget_entry"
    NODE_WIDGET_MENU_BUTTON = "node_widget_menu_button"
    NODE_WIDGET_MENU_ITEM = "node_widget_menu_item"


class DynamicStyle:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # styles dictionary
        self.styles_dictionary = {}

        # set style for node widgets
        self._set_node_widget_style()

    def _set_node_widget_style(self):
        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET] = {
            "width": 130,
            "height": 130,
            "pady": 5,
          #  "fg_color" : "#3C3F41"
            "background": "#3C3F41"
        }

        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_ID] = {
            "font": ("MonoLisa", 10),
        }

        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_LABEL] = {
            "font": ("MonoLisa", 8)
        }

        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_ENTRY] = {
            "font": ("MonoLisa", 10),
        }

        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_MENU_BUTTON] = {
            "font": ("Fedora", 8, ""),
            "text" : "Edit",
            'padx' : 0,
        "background" : "#3F4244",
        "foreground" : "white",
        "highlightbackground" : "grey",
        "highlightthickness" : 1,
        "pady" : 0,
        }

        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_MENU_ITEM] = {
            "font": ("Fedora", 10, ""),
            "padx" : 10,
            "background" : "#3C3F41",
            "foreground" : "#d3d3d3",
            "pady" : 2
        }

    def node_widget_zoom_effect(self,sign_delta):
        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET]["width"] += sign_delta*20
        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET]["height"] += sign_delta * 20

        id_font = self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_ID]["font"]
        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_ID]["font"] = (
        id_font[0], id_font[1] + sign_delta)

        label_font = self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_LABEL]["font"]
        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_LABEL]["font"] = (label_font[0],label_font[1]+sign_delta)

        entry_font = self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_ENTRY]["font"]
        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_ENTRY]["font"] = (
        entry_font[0], entry_font[1] + sign_delta)

        menu_font = self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_MENU_BUTTON]["font"]
        self.styles_dictionary[DynamicWidgetStyles.NODE_WIDGET_MENU_BUTTON]["font"] = (
            menu_font[0], menu_font[1] + sign_delta)

    def get_style(self, widget_key: DynamicWidgetStyles, key=None):
        if key is not None:
            return self.styles_dictionary[widget_key][key]
        return self.styles_dictionary[widget_key]

    def set_style(self, widget_key: DynamicWidgetStyles, key,value):
        self.styles_dictionary[widget_key][key] = value