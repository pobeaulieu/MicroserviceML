def save_microservices_to_txt(fuzzy_clusters, communities, filename):
    """Saves and prints the clustered services and their corresponding classes to a file in a readable format.

    Parameters:
    fuzzy_clusters (dict): Dictionary with services as keys and lists of tuples (cluster id, membership value) as values.
    communities (pd.DataFrame): DataFrame with class names and their corresponding services.
    filename (str): The name of the file to which the clusters and services will be saved.
    """
    # Determine the unique clusters
    unique_clusters = set()
    for memberships in fuzzy_clusters.values():
        for cluster_id, _ in memberships:
            unique_clusters.add(cluster_id)
    unique_clusters = sorted(unique_clusters)

    # Open the file to write the microservice clusters
    with open(filename, "w") as file:
        for cluster_num in unique_clusters:
            # Prepare the cluster header
            cluster_header = f"Microservice {cluster_num[7:]}:\n"
            
            # Write and print the cluster header
            file.write(cluster_header)

            # Find services that belong to the current cluster
            cluster_services = [service for service, memberships in fuzzy_clusters.items() if any(cluster_id == cluster_num for cluster_id, _ in memberships)]
            for service in cluster_services:
                service_entry = f"  - Service: {service}\n"
                
                # Write and print the service entry
                file.write(service_entry)

                # Get related classes for the service from the communities dataframe
                related_classes = communities[communities['service'] == service]['class_name'].tolist()
                for related_class in related_classes:
                    class_entry = f"      * Class: {related_class}\n"
                    
                    # Write and print the class entry
                    file.write(class_entry)
            file.write("\n")

def save_microservices_to_csv(fuzzy_clusters, communities, csv_filename):
    """Saves and prints the clustered services and their corresponding classes to a file in a readable format.

    Parameters:
    fuzzy_clusters (dict): Dictionary with services as keys and lists of tuples (cluster id, membership value) as values.
    communities (pd.DataFrame): DataFrame with class names and their corresponding services.
    filename (str): The name of the file to which the clusters and services will be saved.
    csv_filename (str): The name of the CSV file to which class names will be saved.
    """
    # Determine the unique clusters
    unique_clusters = set()
    for memberships in fuzzy_clusters.values():
        for cluster_id, _ in memberships:
            unique_clusters.add(cluster_id)
    unique_clusters = sorted(unique_clusters)

    # Open the file to write the microservice clusters
    with open(csv_filename, "w") as csv_file:
        for cluster_num in unique_clusters:
            # Find services that belong to the current cluster
            cluster_services = [service for service, memberships in fuzzy_clusters.items() if any(cluster_id == cluster_num for cluster_id, _ in memberships)]
            for service in cluster_services:
                # Get related classes for the service from the communities dataframe
                related_classes = communities[communities['service'] == service]['class_name'].tolist()
                 # Write the class names to the CSV file, separated by commas
                csv_file.write(",".join(related_classes))


    
            csv_file.write("\n")