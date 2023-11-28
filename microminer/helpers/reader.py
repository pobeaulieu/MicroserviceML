import pandas as pd
import os
import json

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

def load_class_labels(system, version='v_imen'):
    def process_file(filepath, label):
        with open(filepath, 'r') as f:
            for line in f:
                class_labels[line.strip()] = label

    class_labels = {}
    
    base_path = "ground_truths/{}/{}".format(version, system)
    files = [
        ("/classes/application.txt", 0),
        ("/classes/utility.txt", 1),
        ("/classes/entity.txt", 2)
    ]

    for file_path, label in files:
        process_file(base_path + file_path, label)

    return class_labels

def load_results(results_file='results/results.json'):
    with open(results_file, 'r') as file:
        results_dict = json.load(file)

    return results_dict

def load_services_from_csv(system, version, data_type):
    """
    Load CSV data for services or microservices.
    - system: The system name.
    - version: The version of the system.
    - data_type: Either 'services' or 'microservices'.
    """
    base_path = os.path.join("ground_truths", version, system)

    def read_csv(file_path):
        """ Utility function to read CSV file and process lines. """
        with open(file_path, 'r') as file:
            # Filter out empty elements and lines
            return [list(filter(None, line.strip().split(','))) for line in file if line.strip()]

    if data_type == 'services':
        service_types = ["application", "utility", "entity"]
        data = {}
        for service_type in service_types:
            file_path = os.path.join(base_path, "services", f"{service_type}.csv")
            lines = read_csv(file_path)
            data[f'{service_type}Services'] = [{'service': [{'className': name} for name in line]} for line in lines]
        return data

    elif data_type == 'microservices':
        file_path = os.path.join(base_path, "microservices", "microservices.csv")
        microservices = read_csv(file_path)
        return microservices

    else:
        raise ValueError("Invalid data_type. Choose 'services' or 'microservices'.")

