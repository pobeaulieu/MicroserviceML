import pandas as pd
import os

def load_call_graph(path_to_call_graph: str) -> pd.DataFrame:
    """Load the call graph."""
    call_graph = pd.read_csv(
        path_to_call_graph,
        delimiter=';',
        header=None,
        names=['class1', 'class2', 'static_distance']
    )
    return call_graph

def load_class_code_from_directory(training_system_name=None):
    if training_system_name:
        root_folder = f"src_code/{training_system_name}/src_code_formatted/"
    else:
        root_folder = f"src_code/tmp/src_code_formatted/"

    def read_java_file(file_path):
        with open(file_path, encoding="ISO-8859-1", errors="ignore") as java_file:
            return java_file.read()

    class_code = {
        file[:-5] if file.endswith(".java") else file: read_java_file(os.path.join(root_folder, file))
        for file in os.listdir(root_folder)
    }   

    return class_code

def get_number_of_classes():
    """Returns the number of classes in the system."""
    return len(load_class_code_from_directory())