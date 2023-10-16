import os
import numpy as np
import csv


def load_class_code_from_directory(system):
    root_folder = './src_code/' + system + '/src_code_formatted/'

    def read_java_file(file_path):
        with open(file_path, encoding="ISO-8859-1", errors="ignore") as java_file:
            return java_file.read()

    class_code = {file.replace(".java", ""): read_java_file(os.path.join(root_folder, file))
                  for file in os.listdir(root_folder)}

    return class_code


def load_data_from_csv(filename):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        class_names, labels, embeddings = [], [], []
        for row in reader:
            class_names.append(row[0])
            label = int(row[1]) if len(row) == 3 else -1
            embedding_str = row[2] if len(row) == 3 else row[1]
            
            labels.append(label)
            embeddings.append(np.array(list(map(float, embedding_str.split(',')))))
        return class_names, labels, embeddings


def write_embeddings_to_csv(version, system, model_type, class_embeddings, class_labels=None):
    """
    Writes embeddings and labels to a CSV file.

    :param version: Version string
    :param system: System string
    :param model_type: Model type string
    :param class_embeddings: Dictionary containing embeddings for each class.
    :param class_labels: Dictionary containing labels for each class. If None, all labels are set to -1.
    """

    file_name = f"./generated_data/embedding/{version}_{system}_{model_type}_embeddings.csv"

    with open(file_name, 'w') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        # If class_labels is not provided, default all labels to -1
        if class_labels is None:
            class_labels = {}

        # Match class_labels with class_embeddings based on key (class name) and write together to csv
        for key, embedding in class_embeddings.items():
            # Convert numpy array to comma-separated string
            embedding_str = ','.join(map(str, embedding))
            writer.writerow([key, class_labels.get(key, -1), embedding_str])

# Example usage:
# class_embeddings = {'class1': [0.5, 0.5], 'class2': [0.7, 0.3]}
# save_embeddings_to_csv('v1', 'system1', 'modelA', class_embeddings)  # This will default all labels to -1


def associate_classes_to_types(version, system):
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


def write_call_graph_to_csv(matrix, version, system):
    csv_filename = f"./generated_data/graph/call/{version}_{system}_call_graph.csv"

    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['class1', 'class2', 'static_distance'])
        for class1 in matrix:
            for class2 in matrix[class1]:
                csv_writer.writerow([class1, class2, matrix[class1][class2]])