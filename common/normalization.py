# Functions to normalize data

def normalize_column(df, column_name):
    """Normalize values of a dataframe column between 0 and 1."""
    column_min = df[column_name].min()
    column_max = df[column_name].max()
    df[column_name] = (df[column_name] - column_min) / (column_max - column_min)
    return df


def filter_and_normalize_distances(df, class_labels_dict):
    """Filter rows based on class labels and normalize specified columns."""
    valid_class_labels = set(class_labels_dict.keys())
    filtered_df = df[df['class1'].isin(valid_class_labels) & df['class2'].isin(valid_class_labels)]
    
    if 'semantic_distance' in filtered_df.columns:
        filtered_df = normalize_column(filtered_df, 'semantic_distance')
    if 'static_distance' in filtered_df.columns:
        filtered_df = normalize_column(filtered_df, 'static_distance')
    
    return filtered_df


def normalize_distances(distances):
    """
    Normalize a dictionary of distance values to a range of 0 to 1.
    
    Parameters:
    - distances (dict): Dictionary of distance values to normalize.
    
    Returns:
    - dict: Normalized distances.
    """
    min_val, max_val = min(distances.values()), max(distances.values())
    range_val = max_val - min_val
    return {k: (v - min_val) / range_val for k, v in distances.items()} if range_val else {k: 0 for k, v in distances.items()}


def normalize_memberships(memberships):
    """
    Normalize membership values so that they sum to 1 for each node.

    Parameters:
    - memberships (dict): A dictionary with nodes as keys and lists of (cluster, membership) tuples as values.

    Returns:
    - dict: Normalized membership values.
    """
    normalized_memberships = {}
    for node, membership_values in memberships.items():
        total_membership = sum(membership for _, membership in membership_values)
        normalized_memberships[node] = [
            (cluster, membership / total_membership if total_membership else 0)
            for cluster, membership in membership_values
        ]
    return normalized_memberships