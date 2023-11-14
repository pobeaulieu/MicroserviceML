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