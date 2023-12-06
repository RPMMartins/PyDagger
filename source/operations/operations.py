from source.dag.dag import DAG
from importlib import import_module
from pathlib import Path
import sys


class Operations:
    def __init__(self,dag: DAG, project_path):
        self.dag = dag
        self.operations = {}
        self.project_path = project_path
        self.data_container = None

    def run_operations(self):
        sys.path.append(str(self.project_path))

        operations_order = self.dag.top_sort()
        for node_id in operations_order:

            name,operation_class, operation_module = self.operations[node_id].values()

            # Dynamically import the module
            module = import_module(operation_module.replace('/', '.'))

            # You can also check if the class exists in the module
            if hasattr(module, operation_class):
                # Do something with the class
                operation = getattr(module, operation_class)()
                operation.add_data_container(self.data_container)
                print("------------------------------")
                print(f"Running Operation: {name}")
                print(f"Id: {node_id}")
                print(f"Class: {operation_class}")
                print(f"Module: {operation_module}")
                operation.execute()
                self.data_container = operation.data_container

            else:
                error_message = f"Class {operation_class} not found in module {operation_class}"
                raise ValueError(error_message)



    def add_operation(self,node_id,name,operation_class,operation_module):
        self.operations[node_id] = {"name": name,
                                    "operation_class": operation_class,
                                    "operation_module": operation_module}

    @classmethod
    def run_dag_from_path(cls,dag_xml_path):
        raise NotImplementedError


class Operation:
    def __init__(self):
        self.data_container = None

    def add_data_container(self,data_container):
        self.data_container = data_container

    def execute(self):
        pass