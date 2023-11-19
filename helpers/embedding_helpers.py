import csv
from helpers.class_helpers import load_class_code_from_directory
from embedding.embeddings import generate_embeddings_for_java_code, generate_word_embeddings_for_java_code
from config.device_setup import set_device
import numpy as np


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


def write_embeddings_to_csv(version, system, model_type, class_embeddings, class_labels=None):
    """
    Writes embeddings and labels to a CSV file.

    :param version: Version string
    :param system: System string
    :param model_type: Model type string
    :param class_embeddings: Dictionary containing embeddings for each class.
    :param class_labels: Dictionary containing labels for each class. If None, all labels are set to -1.
    """

    file_name = f"./generated_data/class_embeddings/{version}_{system}_{model_type}_embeddings.csv"

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

def create_class_embeddings_for_system(system, model_type, model, tokenizer, is_pipeline = False):
    """
    Creates embeddings for all classes in a system.

    :param system: System string
    :param model_type: Model type string
    :param model: Model object
    :param tokenizer: Tokenizer object
    :return: Dictionary containing embeddings for each class.
    """
    # If embeddings already exist, load them from CSV, skip the rest
    class_code = load_class_code_from_directory(system, is_pipeline)
    if model_type == "word2vec":
        class_embeddings = {class_name: generate_word_embeddings_for_java_code(code, model, tokenizer) for class_name, code in class_code.items()}
    else:
        class_embeddings = {class_name: generate_embeddings_for_java_code(code, model, tokenizer, set_device()) for class_name, code in class_code.items()}

    return class_embeddings