import pandas as pd

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

def format_services(data):
    def format_service_list(service_lists):
        return [{"service": [{"className": class_name} for class_name in sublist]} for sublist in service_lists]

    formatted_data = {
        "applicationServices": format_service_list(data.get('Application', [])),
        "entityServices": format_service_list(data.get('Entity', [])),
        "utilityServices": format_service_list(data.get('Utility', []))
    }

    return formatted_data