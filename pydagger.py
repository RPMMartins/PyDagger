import sys
from source.main import main
from source.operations.operations import Operation

system_arguments = sys.argv
if len(system_arguments) < 2:
    raise ValueError("No flags were detected, run any of the following flags: createproject, editproject, rundag")

if __name__ == "__main__":
    system_arguments = sys.argv
    main(system_arguments)
