def map_class_labels_to_categories(class_labels_dict):
    """
    Maps class labels to their respective categories: application, entity, and utility classes.
    Takes a dictionary where keys are class names and values are their corresponding labels.
    """
    application_classes = []
    entity_classes = []
    utility_classes = []

    for class_name, class_label in class_labels_dict.items():
        class_info = {"className": class_name}
        if class_label == 0:
            application_classes.append(class_info)
        elif class_label == 1:
            utility_classes.append(class_info)
        elif class_label == 2:
            entity_classes.append(class_info)

    return {
        "applicationClasses": application_classes,
        "entityClasses": entity_classes,
        "utilityClasses": utility_classes
    }

def map_classes_to_services(communities):
    """
    Create a mapping from each class to its corresponding service.

    Parameters:
    - communities (dict): Dictionary containing lists of service lists.

    Returns:
    - dict: Mapping of class names to service names.
    """
    class_to_service_map = {}
    for service_type, services in communities.items():
        for service_index, service_classes in enumerate(services):
            service_name = f"{service_type} Service {service_index + 1}"
            for class_name in service_classes:
                class_to_service_map[class_name] = service_name
    return class_to_service_map


def map_classes_to_type_labels(version, system):
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