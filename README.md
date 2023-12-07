# PyDagger
Directed Acyclic Graphs (DAG) Python Tkinter Editor Project which schedules python code execution.

This project is currently under devolopment.

To use it in its currenct state run the following:
    1. pip install -r requirements.txt
    2. python pydagger createproject "project_name"
    3. python pydagger editproject "project_name"
    4. Go to dag/"project_name".xml right click and click on "Render Dag"
    5. Play Around with the DAG, you can move the nodes, drag the DAG, zoom in/out, add nodes.
    6. For each node fill the following:
              1. Name: Could be anything, moslty for labelling purposes
              2. Operation: Python class (child of Operator Class) that contains code that will be ran by the DAG.
              3. Location: File Location within the project that contains the Operator Class

        For each operator class write the following:

            from pydagger import Operation
            
            class ExampleOperation(Operation):
                def execute(self):
                    print("data")

        Always include an "execute" method, this will be called by the DAG, in addition, Operation class contains an "data_container" attribute that will be given to the child nodes. e.g.

            from pydagger import Operation
            
            class ExampleOperation(Operation):
                    def execute(self):
                        print(self.data_container)

The following features are being implemented:
                1. Render DAGs. - Done
                2. Move DAGs with mouse drag and mouse wheel. - Done
                3. Zoom in/out DAGs. - Done
                4. Drag Nodes with mouse drag with adaptive edges. - Done
                5. Adding Child/Parent Nodes to any node. - Done
                6. Add edges between any nodes (without creating cycles).
                7. Remove edges/nodes.
                8. Execute Python in Accordance to the DAG. - Done
                9. Save DAG changes both dependencies/style.
                10. Add layer assignment for nodes. - Done
                11. Use Heuristic Methods for edge crossing reduction.
