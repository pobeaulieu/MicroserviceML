# Utility functions for graphs
import pandas as pd
import numpy as np
import networkx as nx


def remove_self_loops(graph):
    """
    Remove self loops from a graph.

    Parameters:
        graph (networkx.Graph): The graph with nodes and edge weights.
    """
    graph.remove_edges_from(nx.selfloop_edges(graph))


def remove_zero_weight_edges(graph):
    """
    Remove edges with zero weight from a graph.

    Parameters:
        graph (networkx.Graph): The graph with nodes and edge weights.
    """
    graph.remove_edges_from([
        (u, v) for u, v, weight in graph.edges(data='weight') if weight == 0
    ])


def print_graph(graph, data):
    """
    Print the nodes and edge weights of the graph.

    Parameters:
        graph (networkx.Graph): The graph with nodes and edge weights.
    """
    for u, v, weight in graph.edges(data=data):
        print(f"{u} -> {v}: {weight}")


def compute_edge_weight(semantic, static, alpha=0.5):
    """
    Compute the edge weight based on semantic and static similarity.

    Parameters:
        semantic (float): The semantic similarity value between two services.
        static (float): The static similarity value between two services.
        alpha (float): The weight given to the static similarity.

    Returns:
        float: The computed edge weight.
    """
    if not (0 <= semantic <= 1) or not (0 <= static <= 1):
        raise ValueError("Both 'semantic' and 'static' values should be between 0 and 1.")
    
    beta = 1 - alpha
    return alpha * static + beta * semantic


def construct_class_graph(static_df, semantic_df, alpha):
    """
    Adds edges to the graph based on static and semantic distances.

    Parameters:
        class_graph (networkx.Graph): The graph to which edges will be added.
        static_df (pd.DataFrame): DataFrame containing static distances.
        semantic_df (pd.DataFrame): DataFrame containing semantic distances.
        alpha (float): Weight given to the static similarity in edge weight computation.
    """
    G = nx.Graph()
    for _, row in static_df.iterrows():
        class1, class2, static_dist = row['class1'], row['class2'], row['static_distance']
        
        # Fetch the semantic distance for the same class pair
        semantic_row = semantic_df[(semantic_df['class1'] == class1) & (semantic_df['class2'] == class2)]
        semantic_dist = semantic_row['semantic_distance'].iloc[0] if not semantic_row.empty else 0

        # Compute the weight and add the edge
        weight = compute_edge_weight(semantic_dist, static_dist, alpha)
        G.add_edge(class1, class2, weight=weight)

    return G

def construct_service_graph(static_distances, semantic_distances, alpha):
    """
    Create a directed graph based on service pairs and combined distances.

    Parameters:
    - static_distances (dict): Normalized static distances between service pairs.
    - semantic_distances (dict): Normalized semantic distances between service pairs.
    - alpha (float): Weighting factor for combining distances.

    Returns:
    - networkx.DiGraph: The directed graph of service pairs with combined edge weights.
    """
    G = nx.DiGraph()

    for service_pair in static_distances:
        static_dist = static_distances[service_pair]
        semantic_dist = semantic_distances.get(service_pair, 0)  # Default to 0 if not found
        edge_weight = compute_edge_weight(semantic_dist, static_dist, alpha)

        # Add edge to the graph
        G.add_edge(service_pair[0], service_pair[1], weight=edge_weight)

    remove_zero_weight_edges(G)
    nodes_list = list(G.nodes)

    return G, nodes_list


def construct_dissimilarity_matrix(graph):
    """
    Construct a dissimilarity matrix from a graph.

    Parameters:
        graph (networkx.Graph): The graph with nodes and edge weights.

    Returns:
        numpy.ndarray: The dissimilarity matrix for clustering algorithms.
    """
    nodes_list = list(graph.nodes)
    default_distance = 1  # Default value indicating maximum dissimilarity
    
    # Initialize the distance matrix
    distances = {
        node: {node2: default_distance for node2 in nodes_list}
        for node in nodes_list
    }

    # Update the distance matrix with the inverse of the edge weights
    for u, v, data in graph.edges(data=True):
        distances[u][v] = distances[v][u] = 1 - data['weight']

    # Convert the distances dictionary to a DataFrame and then to a matrix
    dissimilarity_matrix = pd.DataFrame(distances).values

    # Set the diagonal of the distance matrix to 0 (distance to self is 0)
    np.fill_diagonal(dissimilarity_matrix, 0)

    return dissimilarity_matrix

