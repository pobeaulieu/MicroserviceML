from phase_1_class_typing import run_class_typing
from phase_2_typed_service_identification import run_typed_service_identification
from phase_3_microservice_identification import run_microservice_identification

import argparse
parser = argparse.ArgumentParser()

# Define choices for each argument
version_choices = ["v_imen", "v_team"]
system_choices = ["jforum", "cargotracker", "petclinic", "pos"]
phase1_model_choices = ["ft_codebert", "codebert"]
phase2_embedding_model_choices = ["word2vec", "albert", "roberta", "bert"]
phase2_clustering_model_choices = ["Louvain", "Infomap", "LabelPropagation", "FastGreedy", "GirvanNewman", "Leiden", "Walktrap"]
phase3_model_choices = ["cmeans", "custom_cmeans", "hierarchical"]
training_systems_choices = ["jforum", "cargotracker", "petclinic", "pos"]
classifier_choices = ['svm', 'knn', 'decision_tree', 'logistic_regression', 'naive_bayes', 'ensemble']

parser.add_argument("--version", help="Version of the dataset to use", type=str, choices=version_choices, default="v_imen")
parser.add_argument("--system", help="System to use", type=str, choices=system_choices, default="pos")
parser.add_argument("--phase1_model", help="Phase 1 model to use", type=str, choices=phase1_model_choices, default="codebert")
parser.add_argument("--phase2_embedding_model", help="Phase 2 embedding model to use", type=str, choices=phase2_embedding_model_choices, default="word2vec")
parser.add_argument("--phase2_clustering_model", help="Phase 2 clustering model to use", type=str, choices=phase2_clustering_model_choices, default="Louvain")
parser.add_argument("--phase3_model", help="Phase 3 model to use", type=str, choices=phase3_model_choices, default="custom_cmeans")
# Add training systems argument (can be multiple)
parser.add_argument("--training_systems", help="Systems to use for training", type=str, choices=training_systems_choices, nargs="+", default=["jforum", "cargotracker", "petclinic" ])
parser.add_argument("--classifier", help="Classifier to use", type=str, choices=classifier_choices, default="svm")

# Example usage:
# python main.py --version v_imen --system pos --phase1_model codebert --phase2_model GirvanNewman --phase3_model custom_cmeans --training_systems jforum cargotracker petclinic --classifier svm


####################################################################################################
# MAIN EXECUTION
####################################################################################################

def main(version, system, training_systems, phase1_model, phase2_embedding_model, phase2_clustering_model, phase3_model, selected_classifier):
    # Run phase 1 (class typing)
    print("Running phase 1...")
    run_class_typing(version, system, training_systems, phase1_model, selected_classifier)
    # Run phase 2 (service clustering)
    print("Running phase 2...")
    run_typed_service_identification(version, system, phase2_embedding_model, phase2_clustering_model)
    # Run phase 3 (microservice identification)
    print("Running phase 3...")
    run_microservice_identification(version, system, phase2_embedding_model, phase2_clustering_model, phase3_model)


if __name__ == "__main__":
    args = parser.parse_args()
    version = args.version
    system = args.system
    phase1_model = args.phase1_model
    phase2_embedding_model = args.phase2_embedding_model
    phase2_clustering_model = args.phase2_clustering_model
    phase3_model = args.phase3_model
    training_systems = args.training_systems
    selected_classifier = args.classifier

    main(version, system, training_systems, phase1_model, phase2_embedding_model, phase2_clustering_model, phase3_model, selected_classifier)