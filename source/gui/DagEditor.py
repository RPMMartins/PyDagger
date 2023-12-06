import tkinter as tk
from tkinter import ttk
from collections import defaultdict
from source.gui.nodewidget import NodeWidget
import numpy as np
from source.gui.style import DynamicStyle, DynamicWidgetStyles
from source.fields.fields import OperationFields
from source.operations.operations import Operations
from pathlib import Path

class DagEditor(ttk.Frame):
    def __init__(self, master, dag, project_name, static_style, dynamic_style: DynamicStyle, **kwargs):
        super().__init__(master, **kwargs)

        # set the dag
        self.dag = dag
        self.project_name = project_name

        # set the styles
        self.static_style = static_style
        self.dynamic_style = dynamic_style

        # set the canvas for the edges
        self.canvas = tk.Canvas(self, background="#282c34")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # create context menu
        self.create_context_menu()
        self.canvas.bind("<ButtonPress-3>", self.show_context_menu)

        # bind mouse scroll to resize
        self.canvas.bind("<MouseWheel>", self._on_mousewheel_vertical)
        self.canvas.bind("<Shift-MouseWheel>", self._on_mousewheel_horizontal)
        self.canvas.bind("<Control-MouseWheel>", self._on_mousewheel_size)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", lambda _: self.config(cursor="arrow"))

        # graph to render
        self.nodes = {}
        self.parent_edges = defaultdict(set)
        self.children_edges = defaultdict(set)

        # current zoom
        self.zoom = 0

    def on_press(self, event):
        self.config(cursor="hand2")
        self.start_delta_x = {}
        self.start_delta_y = {}

        for node_id, node in self.nodes.items():
            self.start_delta_x[node_id] = node.winfo_x() - event.x
            self.start_delta_y[node_id] = node.winfo_y() - event.y

    def on_drag(self, event):
        for node_id, node in self.nodes.items():
            x = event.x + self.start_delta_x[node_id]
            y = event.y + self.start_delta_y[node_id]
            node.place(x=x, y=y)

            height, width = node.winfo_height(), node.winfo_width()

            for children_edge in self.children_edges[node_id]:
                line_coordinates = self.canvas.coords(children_edge)
                line_coordinates[0] = x + int(width / 2)
                line_coordinates[1] = y + height
                self.canvas.coords(children_edge, *line_coordinates)

            # update the coordinates for the parent edges
            for parent_edge in self.parent_edges[node_id]:
                line_coordinates = self.canvas.coords(parent_edge)
                line_coordinates[2] = x + int(width / 2)
                line_coordinates[3] = y
                self.canvas.coords(parent_edge, *line_coordinates)

    def _on_mousewheel_size(self, event):
        delta = event.delta

        # set zoom limits
        if delta > 0 and self.zoom == 6:
            return
        if delta < 0 and self.zoom == -2:
            return

        # get center of canvas
        center = (self.winfo_width()/2,self.winfo_height()/2)

        # scale the edges
        self.canvas.scale(
            "all",
            *center,
            1.1 ** np.sign(delta),
            1.1 ** np.sign(delta),
        )

        # update zoom level
        self.zoom += np.sign(delta)

        # update dynamic style
        self.dynamic_style.node_widget_zoom_effect(np.sign(delta))

        for node_id, node in self.nodes.items():
            node.zoom(delta)
            x = node.winfo_x()
            y = node.winfo_y()
            node.place(x=center[0]+(x-center[0]) * 1.1 ** np.sign(delta),
                       y=center[1]+(y-center[1]) * 1.1 ** np.sign(delta))

        # make sure all nodes are updated
        self.update_idletasks()
        self.canvas.update_idletasks()

        for node_id, node in self.nodes.items():
            height, width = node.winfo_height(), node.winfo_width()
            x = node.winfo_x()
            y = node.winfo_y()

            for children_edge in self.children_edges[node_id]:
                line_coordinates = self.canvas.coords(children_edge)
                line_coordinates[0] = x + int(width / 2)
                line_coordinates[1] = y + height
                self.canvas.coords(children_edge, *line_coordinates)

            # update the coordinates for the parent edges
            for parent_edge in self.parent_edges[node_id]:
                line_coordinates = self.canvas.coords(parent_edge)
                line_coordinates[2] = x + int(width / 2)
                line_coordinates[3] = y
                self.canvas.coords(parent_edge, *line_coordinates)

    def _on_mousewheel_vertical(self, event):
        delta = int(-1 * (event.delta / 120))
        for node_id, node in self.nodes.items():
            x = node.winfo_x()
            y = node.winfo_y()
            node.place(x=x, y=y - delta * 75)

            # update the edge coordinates
            for children_edge in self.children_edges[node_id]:
                line_coordinates = self.canvas.coords(children_edge)
                line_coordinates[1] = line_coordinates[1] - delta * 75
                line_coordinates[3] = line_coordinates[3] - delta * 75
                self.canvas.coords(children_edge, *line_coordinates)

    def _on_mousewheel_horizontal(self, event):
        delta = int(-1 * (event.delta / 120))
        for node_id, node in self.nodes.items():
            x = node.winfo_x()
            y = node.winfo_y()
            node.place(x=x - delta * 75, y=y)

            # update the coordinates for the children edges
            for children_edge in self.children_edges[node_id]:
                line_coordinates = self.canvas.coords(children_edge)
                line_coordinates[0] = line_coordinates[0] - delta * 75
                line_coordinates[2] = line_coordinates[2] - delta * 75
                self.canvas.coords(children_edge, *line_coordinates)

    def get_new_node_id(self):
        return max(self.nodes.keys()) + 1

    def add_node(self, x, y, id, operation_name, operation_class, operation_module):
        node = NodeWidget(
            self, id=id,
            name=operation_name,
            operation=operation_module,
            location=operation_class,
            dynamic_style = self.dynamic_style
        )
        node.place(x=x, y=y)
        node.lift()
        self.update()
        self.nodes[id] = node

    def add_edge(self, parent_node_id, child_id):
        parent_node = self.nodes[parent_node_id]
        child_node = self.nodes[child_id]

        # set the edge coordinates from the parent node
        x1, y1 = parent_node.winfo_x(), parent_node.winfo_y()
        height_parent, width_parent = (
            parent_node.winfo_height(),
            parent_node.winfo_width(),
        )
        x1 = x1 + int(width_parent / 2)
        y1 = y1 + height_parent

        # set the edge coordinates to the child node
        x2, y2 = child_node.winfo_x(), child_node.winfo_y()
        width_child = child_node.winfo_width()
        x2 = x2 + int(width_child / 2)

        line_edge = self.canvas.create_line(x1, y1, x2, y2, width=3, arrow=tk.LAST)

        self.children_edges[parent_node_id].add(line_edge)
        self.parent_edges[child_id].add(line_edge)

    def render_dag(self):
        layers = self.dag.set_layers()

        # add and render the nodes
        for level, layer in layers.items():
            index = 0
            for node_id in layer:
                self.add_node(
                    x=200 + index * 220,
                    y=270 * level + 50,
                    id=node_id,
                    **self.dag.xml_operations[node_id]
                )
                index += 1

        # add and render the edges
        for parent_node_id, edges in self.dag.graph.items():
            for edge in edges:
                child_id = edge[0]
                self.add_edge(parent_node_id, child_id)

    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(
            label="New Node", command=lambda: print("New Node")
        )
        self.context_menu.add_command(
            label="New Edge", command=lambda: print("New Edge")
        )
        self.context_menu.add_command(
            label="Rename Dag", command=lambda: print("Rename File")
        )
        self.context_menu.add_command(
            label="Save Dag", command=lambda: print("Save Dag")
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Run Dag", command=self.run_dag)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.context_menu.grab_release()

    def run_dag(self):
        operations = Operations(self.dag,Path(Path.cwd(), self.project_name))

        for node_id, node in self.nodes.items():
            operations.add_operation(node_id,
                                     node.name.get(),
                                     node.operation.get(),
                                     node.location.get()
                                     )
        operations.run_operations()
