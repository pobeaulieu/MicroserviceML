from microminer.interface import MicroMinerInterface
from typing import List, Dict, Union

from microminer.helpers.app_cloner import clone_and_copy_java_contents, remove_tmp_dir

# Imports for phase 1
from microminer.embedding.embedding_model import select_model_and_tokenizer
from microminer.embedding.embeddings import create_class_embeddings_for_system
from microminer.helpers.mapper import map_class_labels_to_categories
from microminer.classification.classifiers import load_classifier_from_pickle

# Imports for phase 2
from microminer.helpers.reader import load_call_graph
from microminer.common.distances import compute_semantic_distances_for_class_pairs
from microminer.common.normalization import filter_and_normalize_distances
from microminer.community_detection.community_detection import CommunityDetection
from microminer.community_detection.community_tuning import fine_tune_communities
from microminer.common.graphs import construct_class_graph
from microminer.helpers.formatter import format_services, format_microservices

# Imports for phase 3
from microminer.common.graphs import construct_dissimilarity_matrix, construct_service_graph
from microminer.clustering.cluster_analysis import assign_clusters_based_on_comparative_ratios, merge_overlapping_clusters, identify_standalone_services
from microminer.common.normalization import normalize_memberships
from microminer.common.distances import compute_static_distances_for_service_pairs, compute_semantic_distances_for_service_pairs
from microminer.clustering.clustering import cluster_services
from microminer.helpers.mapper import map_classes_to_services

# Imports for training models
from microminer.classification.data_processing import prepare_training_data
from microminer.helpers.reader import load_class_labels
from microminer.classification.classifiers import create_classifiers, train_classifiers, save_classifiers_to_pickle


class MicroMinerPipeline(MicroMinerInterface):
    def clone_and_prepare_src_code(self) -> bool:
        print("Cloning Repository...")
        return clone_and_copy_java_contents(self.github_url)

    def execute_phase_1(self) -> Dict[str, List[Dict[str, str]]]:
        print("Phase 1 started...")
        tokenizer, model = select_model_and_tokenizer(self.embeddings_model_name_phase_1)

        print("Creating embeddings...")
        self.embeddings_phase_1, self.num_classes = create_class_embeddings_for_system(self.embeddings_model_name_phase_1, model, tokenizer)

        print("Load classifier and predict...")
        classifier = load_classifier_from_pickle(self.embeddings_model_name_phase_1, self.classification_model_name_phase_1)

        print("Predicting class type...")
        predictions = classifier.predict(list(self.embeddings_phase_1.values()))

        self.labels = dict(zip(self.embeddings_phase_1.keys(), predictions))

        self.result_phase_1 = map_class_labels_to_categories(self.labels)


    def execute_phase_2(self) -> Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]:
        print("Phase 2 started...")

        # Initialize tokenizer and model
        tokenizer, model = select_model_and_tokenizer(self.embeddings_model_name_phase_2)

        print("Creating embeddings...")
        self.embeddings_phase_2, _ = create_class_embeddings_for_system(
            self.embeddings_model_name_phase_2,
            model, 
            tokenizer, 
            is_phase_2=True
        )

        # Compute semantic distances
        print("Computing semantic distances...")
        semantic_distances_df = compute_semantic_distances_for_class_pairs(self.embeddings_phase_2)

        # Load static distances
        print("Loading static distances...")
        static_distances_df = load_call_graph(self.path_to_call_graph)

        # Normalize and filter distances based on class labels
        print("Normalizing and filtering distances...")
        self.normalized_static_distances_between_classes = filter_and_normalize_distances(static_distances_df, self.labels)
        self.normalized_semantic_distances_between_classes = filter_and_normalize_distances(semantic_distances_df, self.labels)

        # Create the graph for community detection
        print("Creating class graph...")
        class_graph = construct_class_graph(
            self.normalized_static_distances_between_classes, 
            self.normalized_semantic_distances_between_classes, 
            self.alpha_phase_2
        )

        # Community detection
        print("Detecting communities...")
        cd = CommunityDetection(class_graph, self.labels, optimize_hyperparameters_flag=False)
        communities = {label: cd.detect_communities(label, self.clustering_model_name_phase_2) 
                       for label in ['Application', 'Entity', 'Utility']}

        # Community tuning
        print("Tuning communities...")
        self.communities = {label_type: fine_tune_communities(services, class_graph.edges(data='weight')) 
                            for label_type, services in communities.items()}

        # Format the result
        self.result_phase_2 = format_services(self.communities)


    def execute_phase_3(self) -> Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]:
        print("Phase 3 started...")

        print("Computing class to service mapping...")
        class_to_service_map = map_classes_to_services(self.communities)

        print("Computing static and semantic distances...")
        normalized_static_distances_between_services = compute_static_distances_for_service_pairs(
            self.normalized_static_distances_between_classes, class_to_service_map)
        normalized_semantic_distances_between_services = compute_semantic_distances_for_service_pairs(
            self.normalized_semantic_distances_between_classes, class_to_service_map)

        # Construct the service graph
        print("Constructing service graph...")
        service_graph, nodes_list = construct_service_graph(normalized_static_distances_between_services, 
                                                 normalized_semantic_distances_between_services, 
                                                 self.alpha_phase_3)

        # Construct the dissimilarity matrix
        print("Constructing dissimilarity matrix...")
        dissimilarity_matrix = construct_dissimilarity_matrix(service_graph)

        # Cluster the services
        print("Clustering services...")
        memberships = cluster_services(
            dissimilarity_matrix, 
            nodes_list, 
            self.clustering_model_name_phase_3, 
            self.num_classes,
            self.num_clusters, 
            self.max_d
        )
        
        # Normalize the memberships
        print("Normalizing memberships...")
        normalized_memberships = normalize_memberships(memberships)

        # Assign services to clusters based on comparative ratios
        print("Assigning services to clusters...")
        clusters = assign_clusters_based_on_comparative_ratios(normalized_memberships)

        # Identify standalone services
        print("Identifying standalone services...")
        clusters = identify_standalone_services(clusters)

        # Merge overlapping clusters
        print("Merging overlapping clusters...")
        clusters = merge_overlapping_clusters(clusters)

        # Format the result
        self.result_phase_3 = format_microservices(clusters, class_to_service_map)
    
    
    def execute_training_phase(self):
        tokenizer, model = select_model_and_tokenizer(self.embeddings_model_name_phase_1)
        training_systems = []

        for system_name in self.training_system_names:
            system_labels = load_class_labels(system_name, self.version)  # dict of class names to labels
            system_embeddings, _ = create_class_embeddings_for_system(self.embeddings_model_name_phase_1, model, tokenizer, is_phase_2=False, training_system_name=system_name)  # dict of class names to embeddings

            system_data = {
                'system_name': system_name,
                'class_names': list(system_labels.keys()),
                'labels': list(system_labels.values()),
                'embeddings': list(system_embeddings.values())
            }

            training_systems.append(system_data)

        Xtrain, ytrain, _, _, _, _ = prepare_training_data(training_systems)

        classifiers = create_classifiers()
        classifiers = train_classifiers(classifiers, Xtrain, ytrain)
        save_classifiers_to_pickle(classifiers, self.embeddings_model_name_phase_1)


    def get_results(self):
        results = {}
        results['config'] = {}
        results['config']['run_id'] = self.run_id
        results['config']['timestamp'] = self.timestamp
        results['config']['github_url'] = self.github_url
        results['config']['path_to_call_graph'] = self.path_to_call_graph
        results['config']['embeddings_model_name_phase_1'] = self.embeddings_model_name_phase_1
        results['config']['classification_model_name_phase_1'] = self.classification_model_name_phase_1
        results['config']['alpha_phase_2'] = self.alpha_phase_2
        results['config']['embeddings_model_name_phase_2'] = self.embeddings_model_name_phase_2
        results['config']['clustering_model_name_phase_2'] = self.clustering_model_name_phase_2
        results['config']['clustering_model_name_phase_3'] = self.clustering_model_name_phase_3
        results['config']['num_clusters'] = self.num_clusters
        results['config']['max_d'] = self.max_d
        results['config']['alpha_phase_3'] = self.alpha_phase_3
        results['phase_1'] = self.result_phase_1
        results['phase_2'] = self.result_phase_2
        results['phase_3'] = self.result_phase_3

        return results


    def clean_up(self):
        remove_tmp_dir()