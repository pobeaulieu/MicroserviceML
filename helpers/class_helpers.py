import os

def load_class_code_from_directory(system_path, isFullPath = False):
    if not isFullPath:
        root_folder = './src_code/' + system_path + '/src_code_formatted/'
    else:
        root_folder = system_path

    def read_java_file(file_path):
        with open(file_path, encoding="ISO-8859-1", errors="ignore") as java_file:
            return java_file.read()

    class_code = {
        file[:-5] if file.endswith(".java") else file: read_java_file(os.path.join(root_folder, file))
        for file in os.listdir(root_folder)
    }   

    return class_code


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


def get_number_of_classes(system):
    """Returns the number of classes in the system."""
    return len(load_class_code_from_directory(system))