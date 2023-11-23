import pandas as pd
import os
import csv
import numpy as np

def load_call_graph(system):
    """Load the call graph."""
    file_path = f"./generated_data/graphs/call/{system}_call_graph.csv"
    call_graph = pd.read_csv(
        file_path,
        delimiter=';',
        header=None,
        names=['class1', 'class2', 'static_distance']
    )
    return call_graph

def load_class_code_from_directory(system):
    root_folder = f"./src_code/{system}/src_code_formatted/"

    def read_java_file(file_path):
        with open(file_path, encoding="ISO-8859-1", errors="ignore") as java_file:
            return java_file.read()

    class_code = {
        file[:-5] if file.endswith(".java") else file: read_java_file(os.path.join(root_folder, file))
        for file in os.listdir(root_folder)
    }   

    return class_code

def get_number_of_classes(system):
    """Returns the number of classes in the system."""
    return len(load_class_code_from_directory(system))


def load_embeddings_from_csv(filename):
    """
    Loads embeddings and labels from a CSV file.

    :param filename: Name of the CSV file to load.
    :return: class_names, class_labels, class_embeddings
    """
    # First column is class name, second column is label, third column is embedding
    class_names, class_labels, class_embeddings = [], [], []

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=';', quotechar='"')
        for row in reader:
            class_names.append(row[0])
            class_labels.append(row[1])
            class_embeddings.append(row[2])

    # Convert class_labels to integers
    class_labels = [int(label) for label in class_labels]

    # Convert class_embeddings to numpy arrays
    class_embeddings = [np.array(embedding.split(','), dtype=np.float32) for embedding in class_embeddings]

    return class_names, class_labels, class_embeddings