##### Dag Definition #####
from source.tools.xml import read_xml_dag
from collections import defaultdict
from source.fields.fields import OperationFields


class DAG:
    def __init__(self, xml_operations):
        self.permanent_mark = None
        self.temporary_mark = None
        self.stack = None
        self.graph = defaultdict(list)
        self.nodes = set()
        self.xml_operations = xml_operations

    @classmethod
    def read_from_xml(cls, project_path):

        # read all the operations from the test.xml file
        xml_operations = read_xml_dag(project_path)

        graph = cls(xml_operations)

        # add all the edges to the dag object
        for node_id, node_details in xml_operations.items():
            if OperationFields.DEPENDENCIES.value in node_details.keys():
                for parent_node in node_details[OperationFields.DEPENDENCIES.value]:
                    graph.add_edge(parent_node, node_id, 1, check_cyles=False)
                node_details.pop(OperationFields.DEPENDENCIES.value)
        return graph

    def save_to_xml(self):
        raise NotImplementedError

    def add_edge(self, u, v, weight, check_cyles=True):
        self.graph[u].append((v, weight))
        self.nodes.add(u)
        self.nodes.add(v)
        if check_cyles:
            self.top_sort()

    def add_nodes(self, list_of_nodes: list):
        for node in list_of_nodes:
            self.nodes.add(node)

    def add_edges(self, list_of_edges: list[tuple]):
        for edge in list_of_edges:
            self.add_edge(*edge, check_cyles=False)

    def longest_path(self):
        top_order = self.top_sort()
        dist = {v: 0 for v in top_order}
        dist[top_order[0]] = 0

        for vertex in top_order:
            for neighbor, weight in self.graph[vertex]:
                if dist[neighbor] < dist[vertex] + weight:
                    dist[neighbor] = dist[vertex] + weight

        return dist

    def set_layers(self):
        layers = {}
        longest_paths = self.longest_path()

        for node, path_length in longest_paths.items():
            if path_length not in layers.keys():
                layers[path_length] = set()

            layers[path_length].add(node)

        return layers

    def top_sort(self):
        self.permanent_mark = {v: False for v in self.nodes}
        self.temporary_mark = {v: False for v in self.nodes}

        self.stack = []

        for node in self.nodes:
            self.visit(node)

        return self.stack[::-1]

    def visit(self, node):
        # set the permanent_mark and temporary mark when using visit for adding an edge
        if self.permanent_mark is None:
            self.permanent_mark = {v: False for v in self.nodes}
            self.temporary_mark = {v: False for v in self.nodes}

        # check if node has been encountered before
        if self.temporary_mark[node]:
            raise ValueError("This Graph contains Cycles")

        self.temporary_mark[node] = True

        for neighbor, _ in self.graph[node]:
            self.visit(neighbor)

        self.temporary_mark[node] = False
        self.permanent_mark[node] = True
        if node not in self.stack:
            self.stack.append(node)
