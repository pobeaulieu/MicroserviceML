def print_communities(label_type, communities):
    """Print the detected communities."""
    for idx, community in enumerate(communities):
        print(f"{label_type} Service Community {idx + 1}:")
        for class_name in community:
            print(f"  - {class_name}")
        print("=" * 40)
    print("\n")


def save_communities_to_csv(communities, version, system, phase1_model, phase2_model):
    with open(f'generated_data/phase2_service_clustering/{phase2_model}/{version}_{system}_{phase1_model}_communities.csv', 'w') as f:
        f.write('class_name,service\n')
        for label_type, services in communities.items():
            for i, service in enumerate(services):
                for class_name in service:
                    f.write(f'{class_name},{label_type} Service {i + 1}\n')
