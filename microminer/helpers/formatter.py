def format_services(data):
    def format_service_list(service_lists):
        return [{"service": [{"className": class_name} for class_name in sublist]} for sublist in service_lists]

    formatted_data = {
        "applicationServices": format_service_list(data.get('Application', [])),
        "entityServices": format_service_list(data.get('Entity', [])),
        "utilityServices": format_service_list(data.get('Utility', []))
    }

    return formatted_data


def format_microservices(clusters, class_to_service_map):
    # Initialize data structure for microservices
    microservices_data = {}

    for service, cluster_infos in clusters.items():
        # Determine service type
        service_type = ("applicationServices" if "Application" in service 
                        else "entityServices" if "Entity" in service 
                        else "utilityServices" if "Utility" in service 
                        else None)
        if service_type is None:
            continue

        # Get classes for each service
        classes = [{"className": class_name} for class_name, mapped_service in class_to_service_map.items() if mapped_service == service]
        
        # Group services by microservices (clusters)
        for cluster_info in cluster_infos:
            cluster_name = cluster_info[0].replace('cluster', 'microservice')  # Renaming clusters to 'microservice'
            
            if cluster_name not in microservices_data:
                microservices_data[cluster_name] = {"applicationServices": [], "entityServices": [], "utilityServices": []}
            
            microservices_data[cluster_name][service_type].append({"service": classes})

    # Format the final output
    formatted_output = {"microservices": [{"microservice": microservices_data[cluster_name]} for cluster_name in microservices_data]}

    return formatted_output









