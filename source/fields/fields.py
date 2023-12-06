### fields container ###

from enum import Enum


class LocalFolders(str, Enum):
    SOURCE = "source"
    DAG = "dag"
    GUI = "gui"
    CONFIG = "config"


class OperationFields(str,Enum):
    OPERATION_NAME = "operation_name"
    OPERATION_CLASS = "operation_class"
    OPERATION_MODULE = "operation_module"
    DEPENDENCIES = "dependencies"


class FileNames(str, Enum):
    DAG_XML = "test.xml"
