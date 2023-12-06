from xml.etree.ElementTree import Element, ElementTree
from pathlib import Path
import xml.etree.ElementTree as ET

from source.fields.fields import LocalFolders, FileNames


def create_new_dag_xml(project_path, project_name):
    # Create an empty XML element
    root = Element("root")

    # Create an ElementTree object
    tree = ElementTree(root)

    # Set path
    xml_file_path = Path(project_path, LocalFolders.DAG.value, f"{project_name}.xml")

    # Adding new 'operation' elements to the root
    new_operation_1 = ET.Element("operation", name="load data")
    root.append(new_operation_1)
    field1 = ET.SubElement(new_operation_1, "field", name="id", type="int")
    field1.text = "1"
    field2 = ET.SubElement(
        new_operation_1, "field", name="operation_module", type="str"
    )
    field2.text = "loaddata"
    field3 = ET.SubElement(new_operation_1, "field", name="operation_class", type="str")
    field3.text = "LoadData"

    new_operation_2 = ET.Element("operation", name="take mean")
    root.append(new_operation_2)
    field4 = ET.SubElement(new_operation_2, "field", name="dependencies", type="list")
    values = ET.SubElement(field4, "value", type="int")
    values.text = "1"
    field5 = ET.SubElement(new_operation_2, "field", name="id", type="int")
    field5.text = "2"
    field6 = ET.SubElement(
        new_operation_2, "field", name="operation_module", type="str"
    )
    field6.text = "takemean"
    field7 = ET.SubElement(new_operation_2, "field", name="operation_class", type="str")
    field7.text = "TakeMean"

    # Save empty Dag object into xml
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write(xml_file_path, encoding="utf-8")


def read_field(field):
    field_type = field.attrib.get("type")
    if field_type == "str":
        return field.text

    if field_type == "int":
        return int(field.text)

    if field_type == "list":
        values = []
        for field in field.findall("value"):
            values.append(read_field(field))

        return values


def read_xml_dag(xml_file_path) -> dict[int, dict]:
    # Read Xml
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    operations = {}

    # Iterate through each operation
    for operation in root.findall("operation"):
        operation_fields = {"operation_name": operation.attrib["name"]}
        # Iterate through fields within the operation
        for field in operation.findall("field"):
            field_name = field.attrib["name"]
            field_value = read_field(field)
            operation_fields[field_name] = field_value

        operation_id = operation_fields["id"]
        operation_fields.pop("id")
        operations[operation_id] = operation_fields

    return operations
