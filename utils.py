import os
import numpy as np
import csv


def load_class_code_from_directory(system):
    root_folder = './src_code/' + system + '/src_code_formatted/'

    def read_java_file(file_path):
        with open(file_path, encoding="ISO-8859-1", errors="ignore") as java_file:
            return java_file.read()

    class_code = {
        file[:-5] if file.endswith(".java") else file: read_java_file(os.path.join(root_folder, file))
        for file in os.listdir(root_folder)
    }   

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


def print_communities(label_type, communities):
    """Print the detected communities."""
    for idx, community in enumerate(communities):
        print(f"{label_type} Service Community {idx + 1}:")
        for class_name in community:
            print(f"  - {class_name}")
        print("=" * 40)
    print("\n")


def save_communities_to_csv(communities, version, system, algorithm):
    with open(f'generated_data/community/{version}_{system}_{algorithm}_communities.csv', 'w') as f:
        f.write('class_name,service\n')
        for label_type, services in communities.items():
            for i, service in enumerate(services):
                for class_name in service:
                    f.write(f'{class_name},{label_type} Service {i + 1}\n')


def save_microservices_to_file(labels, services_graph, communities_df, filename):
    """Saves the clustered services and related classes to a file."""
    with open(filename, "w") as file:
        for cluster_num in np.unique(labels):
            file.write(f"Microservice {cluster_num + 1}:\n")
            cluster_services = [service_name for idx, service_name in enumerate(services_graph.nodes) if labels[idx] == cluster_num]
            
            for service in cluster_services:
                file.write(f"  - Service: {service}\n")
                related_classes = communities_df[communities_df['service'] == service]['class_name'].tolist()
                for related_class in related_classes:
                    file.write(f"    - Class: {related_class}\n")
            file.write("\n")


def save_clusters_to_file(clusters, communities_df, filename):
    with open(filename, "w") as file:
        for cluster_num, (center, members) in enumerate(clusters.items(), 1):
            file.write(f"Microservice {cluster_num} centered at {center}:\n")
            for service in members:
                file.write(f"  - Service: {service}\n")
                related_classes = communities_df[communities_df['service'] == service]['class_name'].tolist()
                for related_class in related_classes:
                    file.write(f"    - Class: {related_class}\n")
            file.write("\n")