from source.methods.methods import defined_methods


def main(system_arguments):
    if len(system_arguments)<2:
        raise ValueError("No flags were detected, run any of the following flags: createproject")

    # Retrive method flag
    method_flag = system_arguments[1]

    # Check if the method given is well-defined
    if method_flag not in defined_methods:
        raise ValueError(f"Method '{method_flag}' is not defined")

    # Obtain Chosen method
    method = defined_methods[method_flag]

    # Running Method
    method(system_arguments)