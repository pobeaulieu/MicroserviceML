from pipeline import interface
from typing import List, Dict, Union

# from config.device_setup import set_device
# from embedding.embedding_model import select_model_and_tokenizer
# from helpers.embedding_helpers import create_class_embeddings_for_system, load_embeddings_from_csv, write_embeddings_to_csv
# from type_classification.classifiers import load_classifier_from_pickle


# from common.utils import load_call_graph
# from common.distances import compute_semantic_distances_for_class_pairs
# from common.normalization import filter_and_normalize_distances
# import networkx as nx
# from community_detection.community_detection import CommunityDetection
# from community_detection.community_tuning import fine_tune_all_services
# from helpers.service_community_helpers import save_communities_to_csv


class MicroMinerPipeline(interface.MicroMinerInterface):
    # # Phase 1 attributes
    # embeddings_model_name_phase_3 = "bert"
    # classification_model_name = "svm"
    # embeddings_phase_1 = "embeddings_phase_1"

    # # Phase 2 attributes
    # phase_2_cluster_model_name = "louvain"
    # embeddings_phase_2 = "embeddings_phase_2"
    # embeddings_model_name_phase_2 = "word2vec"
    # communities = "communities" # map to return type
    # class_graph = "class_graph"

    # # Phase 3 attributes
    # phase_3_cluster_model_name = "cmeans"
    # service_graph = "service_graph"
    # num_clusters = -1
    # max_d = -1

    def clone_and_prepare_src_code(self, github_url: str) -> bool:
        raise NotImplementedError("This method must be implemented by the subclass.")

    def execute_phase_1(self) -> Dict[str, List[Dict[str, str]]]:
        print("Phase 1 is working !")
        # tokenizer, model = select_model_and_tokenizer(embedding_model)
        # model = model.to(set_device())

        # class_embeddings = create_class_embeddings_for_system(src_code_path, embedding_model, model, tokenizer, True)

        # classifier = load_classifier_from_pickle(embedding_model, classifier_name)
        # prediction = classifier.predict(list(class_embeddings.values()))

        # # TODO : Save embeddings
        # # write_embeddings_to_csv(version, test_system, model_type, class_embeddings, predictions=predictions[selected_classifier])

        # # TODO : Format data and return in the good format
        
        return {
            "applicationClasses": [
                {"className": "x"},
                {"className": "x"}
            ]
        }

    def execute_phase_2(self) -> Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]:
        
        # class_names, class_labels, class_embeddings = load_embeddings_from_csv(embeddings_path)
        # class_labels_dict, class_embeddings_dict = dict(zip(class_names, class_labels)), dict(zip(class_names, class_embeddings))
        # static_df = load_call_graph(call_graph_path)

        # semantic_df = compute_semantic_distances_for_class_pairs(class_embeddings_dict)
        # static_df = filter_and_normalize_distances(static_df, class_labels_dict)
        # semantic_df = filter_and_normalize_distances(semantic_df, class_labels_dict)
        # merged_df = static_df.merge(semantic_df, on=['class1', 'class2'], how='outer')
        # class_graph = merged_df.fillna({'static_distance': 0, 'semantic_distance': 0})

        # G = nx.from_pandas_edgelist(class_graph[class_graph['static_distance'] != 0], 'class1', 'class2', ['static_distance'])
        # cd = CommunityDetection(G, class_labels_dict, optimize_hyperparameters_flag=False)

        # distances = [(row['class1'], row['class2'], row['static_distance']) for _, row in class_graph.iterrows()]  # OR other distances

        # communities = {
        # 'Application': cd.detect_communities('Application', phase2_model),
        # 'Entity': cd.detect_communities('Entity', phase2_model),
        # 'Utility': cd.detect_communities('Utility', phase2_model)
        # }

        # fine_tuned_communities = {
        #     label_type: fine_tune_all_services(services, distances)
        #     for label_type, services in communities.items()
        # }

        # # TODO : Save communities
        # # save_communities_to_csv(fine_tuned_communities, version, system, phase1_model, phase2_model)


        # # TODO : Format data and return in the good format
        
        raise NotImplementedError("This method must be implemented by the subclass.")

def execute_phase_3(self) -> Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]:
        raise NotImplementedError("This method must be implemented by the subclass.")