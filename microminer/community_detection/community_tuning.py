# Functions that fine-tune communities of classes

def fine_tune_cluster(service, services, distance_map):
    score_service = {i: 0 for i in range(len(services))}
    
    for other_service, distance in distance_map.get(service, {}).items():
        for i, s in enumerate(services):
            if other_service in s:
                score_service[i] += distance
    
    max_score = max(score_service.values())
    if max_score > 0:
        max_indices = [i for i, x in enumerate(score_service.values()) if x == max_score]
        if len(max_indices) == 1:
            services[max_indices[0]].append(service)
            services = [s for s in services if s != [service]]

    return services

def fine_tune_communities(services_list, distances):
    distance_map = {s1: {s2: d} for s1, s2, d in distances}
    
    for i, s in enumerate(services_list):
        if len(s) == 1:
            services_list = fine_tune_cluster(s[0], services_list, distance_map)
    return services_list