####################################################################
##### Script Containing Methods for managing PyDagger Projects #####
####################################################################

from pathlib import Path

from source.tools.xml import create_new_dag_xml, read_xml_dag
from source.gui.gui import run_gui_main_loop
from source.fields.fields import LocalFolders
from source.dag.dag import DAG


def get_second_argument(system_arguments,error_message):
    if len(system_arguments) < 3:
        raise ValueError(error_message)
    name = system_arguments[2]
    return name


def get_project_name(system_arguments):
    project_name = get_second_argument(system_arguments,
                                       error_message="No project name was given")
    return project_name


def get_dag_name(system_arguments):
    dag_name = get_second_argument(system_arguments,
                                   error_message="No dag name was given")
    return dag_name


def get_project_path(project_name):
    current_directory = Path.cwd()
    project_path = Path(current_directory, project_name)

    return project_path


def create_project(system_arguments):
    project_name = get_project_name(system_arguments)

    project_path = get_project_path(project_name)

    if project_path.exists():
        raise ValueError("Project name already taken in local folder")

    project_path.mkdir()

    # Populate Project directory with Default folders
    for folder in LocalFolders:
        Path(project_path, folder.value).mkdir()

    # Create empty dag xml file
    create_new_dag_xml(project_path, project_name)


def edit_project(system_arguments):
    project_name = get_project_name(system_arguments)

    project_path = get_project_path(project_name)

    # Check if project exists
    if not project_path.exists():
        raise ValueError("Project name does not exit")

    run_gui_main_loop(project_name)


def run_dag(system_arguments):
    dag_name = get_dag_name(system_arguments)

    print()

# Available methods dictionary
defined_methods = {"createproject": create_project,
                   "editproject": edit_project,
                   "rundag": run_dag}
