# Functions for analyzing clusters
import numpy as np
from itertools import combinations


def assign_clusters_based_on_comparative_ratios(memberships):
    """
    Assign services to clusters based on a comparison of their membership strengths.

    Parameters:
    - memberships (dict): Dictionary of services with their membership values.

    Returns:
    - dict: Cluster assignments based on comparative ratios of membership strengths.
    """
    cluster_assignments = {}

    for service, membership_values in memberships.items():
        if not membership_values:
            continue

        # Sort memberships in descending order of strength
        sorted_memberships = sorted(membership_values, key=lambda x: x[1], reverse=True)
        assigned_clusters = [sorted_memberships[0]]  # Start with the highest membership cluster

        for i in range(1, len(sorted_memberships)):
            current_membership = sorted_memberships[i][1]
            lower_mean = np.mean([m for _, m in sorted_memberships[i+1:]]) if i < len(sorted_memberships) - 1 else 0
            higher_mean = np.mean([m for _, m in sorted_memberships[:i]])

            # Compare ratios to determine cluster assignment
            ratio_with_lower = current_membership / lower_mean if lower_mean > 0 else float('inf')
            ratio_with_higher = current_membership / higher_mean if higher_mean > 0 else float('inf')

            if abs(ratio_with_higher - 1) < abs(ratio_with_lower - 1):
                assigned_clusters.append(sorted_memberships[i])
            else:
                break  # Stop assigning additional clusters

        cluster_assignments[service] = assigned_clusters

    return cluster_assignments

def calculate_overlap(cluster_a, cluster_b):
        """
        Calculate the overlap between two clusters.
        
        Parameters:
        cluster_a (list): The first cluster to compare.
        cluster_b (list): The second cluster to compare.
        
        Returns:
        float: The ratio of the intersection to the union of the two clusters.
        """
        intersection = set(cluster_a).intersection(cluster_b)
        union = set(cluster_a).union(cluster_b)
        return len(intersection) / len(union) if union else 0


def merge_overlapping_clusters(cluster_assignments, overlap_threshold=0.5):
    """
    Merge clusters that have significant overlap in services, and then renumber clusters sequentially.

    Parameters:
    - cluster_assignments (dict): A dictionary mapping services to their cluster memberships.
    - overlap_threshold (float): Threshold to determine significant overlap.

    Returns:
    - dict: Updated cluster assignments after merging overlapping clusters and renumbering.
    """
    # Step 1: Create a mapping of cluster IDs to their services
    cluster_service_map = {}
    for service, memberships in cluster_assignments.items():
        for cluster_name, _ in memberships:
            cluster_id = int(cluster_name[7:])
            cluster_service_map.setdefault(cluster_id, set()).add(service)

    # Step 2: Identify overlapping clusters
    overlapping_clusters = {
        (cluster1, cluster2)
        for cluster1, cluster2 in combinations(cluster_service_map.keys(), 2)
        if calculate_overlap(cluster_service_map[cluster1], cluster_service_map[cluster2]) >= overlap_threshold
    }
    print(f"Overlapping clusters: {overlapping_clusters}")

    # Step 3: Merge overlapping clusters
    merged_clusters = {}
    for cluster1, cluster2 in overlapping_clusters:
        cluster_service_map[cluster1].update(cluster_service_map.pop(cluster2, set()))
        merged_clusters[cluster2] = cluster1

    # Step 4: Renumber clusters sequentially
    cluster_renumbering_map = {original: new for new, original in enumerate(sorted(cluster_service_map), start=1)}

    # Step 5: Update and consolidate cluster memberships
    updated_cluster_assignments = {}
    for service, memberships in cluster_assignments.items():
        updated_memberships = {}
        for cluster_name, membership in memberships:
            cluster_id = int(cluster_name[7:])
            merged_cluster_id = merged_clusters.get(cluster_id, cluster_id)
            new_cluster_id = cluster_renumbering_map[merged_cluster_id]
            updated_cluster_name = f"cluster{new_cluster_id}"
            updated_memberships[updated_cluster_name] = max(updated_memberships.get(updated_cluster_name, 0), membership)
        updated_cluster_assignments[service] = list(updated_memberships.items())

    return updated_cluster_assignments


def identify_standalone_services(cluster_assignments, occurrence_threshold=0.5):
    """
    Identify services that are part of an excessive number of clusters, suggesting they should be standalone microservices.

    Parameters:
    - cluster_assignments (dict): The current cluster assignments of services.

    Returns:
    - dict: Updated cluster assignments with standalone microservices formed.
    """
    # Calculate the total number of unique clusters
    total_clusters = len(set(cluster for memberships in cluster_assignments.values() for cluster, _ in memberships))

    # Set threshold
    max_clusters_per_service = total_clusters * occurrence_threshold

    # Identify services in more clusters than the threshold
    standalone_candidates = {service for service, memberships in cluster_assignments.items() if len(memberships) > max_clusters_per_service}

    print(f"Standalone candidates: {standalone_candidates}")

    # Create standalone microservices for these candidates
    standalone_cluster_id = max(int(cluster[7:]) for memberships in cluster_assignments.values() for cluster, _ in memberships) + 1
    for service in standalone_candidates:
        cluster_assignments[service] = [(f"cluster{standalone_cluster_id}", 1.0)]
        standalone_cluster_id += 1

    # Remove these services from their original clusters
    for service in standalone_candidates:
        for memberships in cluster_assignments.values():
            memberships[:] = [m for m in memberships if m[0] != service]

    return cluster_assignments
