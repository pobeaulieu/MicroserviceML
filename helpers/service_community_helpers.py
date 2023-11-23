def print_communities(label_type, communities):
    """Print the detected communities."""
    for idx, community in enumerate(communities):
        print(f"{label_type} Service Community {idx + 1}:")
        for class_name in community:
            print(f"  - {class_name}")
        print("=" * 40)
    print("\n")


def save_communities_to_csv(communities, version, system, phase1_model, phase2_model):
    with open(f'generated_data/service_communities/{phase2_model}/{version}_{system}_{phase1_model}_communities.csv', 'w') as f:
        f.write('class_name,service\n')
        for label_type, services in communities.items():
            for i, service in enumerate(services):
                for class_name in service:
                    f.write(f'{class_name},{label_type} Service {i + 1}\n')


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
