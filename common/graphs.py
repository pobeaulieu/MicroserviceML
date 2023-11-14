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
