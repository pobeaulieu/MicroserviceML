from pipeline import interface
from typing import List, Dict, Union

from config.device_setup import set_device
from embedding.embedding_model import select_model_and_tokenizer
from helpers.embedding_helpers import create_class_embeddings_for_system
from type_classification.classifiers import load_classifier_from_pickle

from common.utils import load_call_graph
from common.distances import compute_semantic_distances_for_class_pairs
from common.normalization import filter_and_normalize_distances
import networkx as nx
from community_detection.community_detection import CommunityDetection
from community_detection.community_tuning import fine_tune_all_services
from common.utils import format_services


class MicroMinerPipeline(interface.MicroMinerInterface):

    def clone_and_prepare_src_code(self, github_url: str) -> bool:
        raise NotImplementedError("This method must be implemented by the subclass.")

    def execute_phase_1(self) -> Dict[str, List[Dict[str, str]]]:
        print("Phase 1 started...")

        tokenizer, model = select_model_and_tokenizer(self.embeddings_model_name_phase_1)
        model = model.to(set_device())

        print("Creating embeddings...")
        self.embeddings_phase_1 = create_class_embeddings_for_system("pos", self.embeddings_model_name_phase_1, model, tokenizer)

        print("Load classifier and predict...")
        classifier = load_classifier_from_pickle(self.embeddings_model_name_phase_1, self.classification_model_name_phase_1)
        prediction = classifier.predict(list(self.embeddings_phase_1.values()))

        # TODO Extract this in a mapper function
        # TODO not use 2 variables for the same thing, but lazy rn
        pair_class_label = zip(self.embeddings_phase_1.keys(), prediction)
        self.result_phase_1 = list(zip(self.embeddings_phase_1.keys(), prediction))

        application_classes = []
        entity_classes = []
        utility_classes = []

        for class_name, class_label in pair_class_label:
            class_info = {"className": class_name}
            if class_label == '0':
                application_classes.append(class_info)
            elif class_label == '1':
                utility_classes.append(class_info)
            elif class_label == '2':
                entity_classes.append(class_info)

        result = {
            "applicationClasses": application_classes,
            "entityClasses": entity_classes,
            "utilityClasses": utility_classes
        }

        return result

    def execute_phase_2(self) -> Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]:
        print("Phase 2 started...")

        class_names, class_labels = zip(*self.result_phase_1)
        class_labels = [int(label) for label in class_labels]

        class_labels_dict, class_embeddings_dict = dict(zip(class_names, class_labels)), dict(zip(class_names, self.embeddings_phase_1.values()))
        print("Load call graph...")
        static_df = load_call_graph("pos") # static values for debug purposes

        # TODO : Refacto some shit cause there is a lot of useless things here
        print("Create class graph base on static distances...")
        semantic_df = compute_semantic_distances_for_class_pairs(class_embeddings_dict)
        static_df = filter_and_normalize_distances(static_df, class_labels_dict)
        semantic_df = filter_and_normalize_distances(semantic_df, class_labels_dict)
        merged_df = static_df.merge(semantic_df, on=['class1', 'class2'], how='outer')
        self.class_graph = merged_df.fillna({'static_distance': 0, 'semantic_distance': 0})

        G = nx.from_pandas_edgelist(self.class_graph[self.class_graph['static_distance'] != 0], 'class1', 'class2', ['static_distance'])
        cd = CommunityDetection(G, class_labels_dict, optimize_hyperparameters_flag=False)

        distances = [(row['class1'], row['class2'], row['static_distance']) for _, row in self.class_graph.iterrows()]  # OR other distances

        communities = {
        'Application': cd.detect_communities('Application', self.clustering_model_name_phase_2),
        'Entity': cd.detect_communities('Entity', self.clustering_model_name_phase_2),
        'Utility': cd.detect_communities('Utility', self.clustering_model_name_phase_2)
        }

        self.communities = {
            label_type: fine_tune_all_services(services, distances)
            for label_type, services in communities.items()
        }

        return format_services(self.communities)

    def execute_phase_3(self) -> Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]:
        raise NotImplementedError("This method must be implemented by the subclass.")