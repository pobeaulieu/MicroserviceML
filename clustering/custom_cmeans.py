class CustomFuzzyCMeans:
    """
    A custom implementation of the Fuzzy C-Means clustering algorithm.

    Attributes:
        center_type_indices: A dict mapping the service type to its index.
    """
    def __init__(self):
        self.center_type = 'Application'
        self.center_type_indices = {}

    def calculate_membership(self, service_idx, center_idx, distances):
        """
        Calculate the fuzzy membership of a service to a cluster center.
        
        Parameters:
        service_idx (int): Index of the service for which membership is being calculated.
        center_idx (int): Index of the cluster center to which membership is being calculated.
        distances (list): Matrix of distances between services and cluster centers.
        
        Returns:
        float: The membership value of the service to the cluster center.
        """
        epsilon = 1e-10  # Small value to avoid division by zero.
        distance_to_center = distances[service_idx][center_idx]

        membership_sum = 0.0

        if distance_to_center == 0:
            return 1.0
        
        for other_center_idx in self.center_type_indices.values():
            if other_center_idx != service_idx:
                # Direct distances to other centers
                other_distance_to_center = distances[service_idx][other_center_idx]

                membership_ratio = distance_to_center / (other_distance_to_center + epsilon)
                membership_sum += membership_ratio ** 2

        # The membership value is the inverse of the sum, normalized by the number of centers
        return 1 / membership_sum if membership_sum > 0 else 0

        
    def cluster_services(self, services_list, distances):
        """
        Cluster services based on their membership values to each cluster center.

        Parameters:
        services_list (list): List of all services to be clustered.
        distances (list): Matrix of distances between services and cluster centers.

        Returns:
        dict: A dictionary with services as keys and lists of (cluster, membership) tuples as values.
        """

        self.center_type_indices = {
            service: idx for idx, service in enumerate(services_list) if service.startswith(self.center_type)
        }
        
        # Calculate raw membership values for each service to each cluster center
        memberships = {}
        for service_idx, service in enumerate(services_list):
            service_memberships = []
            for idx, (_, center_idx) in enumerate(self.center_type_indices.items()):
                membership_value = self.calculate_membership(service_idx, center_idx, distances)
                service_memberships.append((f"cluster{idx+1}", membership_value))
            memberships[service] = service_memberships

        return memberships