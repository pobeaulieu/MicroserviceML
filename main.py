from phase_1_class_typing import run_class_typing
from phase_2_typed_service_identification import run_typed_service_identification
from phase_3_microservice_identification import run_microservice_identification

import argparse
parser = argparse.ArgumentParser()

# Define choices for each argument
version_choices = ["v_imen", "v_team"]
system_choices = ["jforum", "cargotracker", "petclinic", "pos"]
phase1_model_choices = ["ft_codebert", "word2vec", "albert", "codebert", "roberta", "bert"]
phase2_model_choices = ["Louvain", "Infomap", "LabelPropagation", "FastGreedy", "GirvanNewman", "Leiden", "Walktrap"]
phase3_model_choices = ["cmeans", "custom_cmeans", "hierarchical"]
training_systems_choices = ["jforum", "cargotracker", "petclinic", "pos"]
classifier_choices = ['svm', 'knn', 'decision_tree', 'logistic_regression', 'naive_bayes', 'ensemble']

parser.add_argument("--version", help="Version of the dataset to use", type=str, choices=version_choices, default="v_imen")
parser.add_argument("--system", help="System to use", type=str, choices=system_choices, default="pos")
parser.add_argument("--phase1_model", help="Phase 1 model to use", type=str, choices=phase1_model_choices, default="codebert")
parser.add_argument("--phase2_model", help="Phase 2 model to use", type=str, choices=phase2_model_choices, default="GirvanNewman")
parser.add_argument("--phase3_model", help="Phase 3 model to use", type=str, choices=phase3_model_choices, default="custom_cmeans")
# Add training systems argument (can be multiple)
parser.add_argument("--training_systems", help="Systems to use for training", type=str, choices=training_systems_choices, nargs="+", default=["jforum", "cargotracker", "petclinic"])
parser.add_argument("--classifier", help="Classifier to use", type=str, choices=classifier_choices, default="svm")

# Example usage:
# python main.py --version v_imen --system pos --phase1_model codebert --phase2_model GirvanNewman --phase3_model custom_cmeans --training_systems jforum cargotracker petclinic --classifier svm


####################################################################################################
# MAIN EXECUTION
####################################################################################################

def main(version, system, phase1_model, phase2_model, phase3_model, selected_classifier):
    # Run phase 1 (class typing)
    run_class_typing(training_systems, version, system, phase1_model, selected_classifier)
    # Run phase 2 (service clustering)
    run_typed_service_identification(version, system, phase1_model, phase2_model)
    # Run phase 3 (microservice identification)
    run_microservice_identification(version, system, phase1_model, phase2_model, phase3_model)


if __name__ == "__main__":
    args = parser.parse_args()
    version = args.version
    system = args.system
    phase1_model = args.phase1_model
    phase2_model = args.phase2_model
    phase3_model = args.phase3_model
    training_systems = args.training_systems
    selected_classifier = args.classifier

    main(version, system, phase1_model, phase2_model, phase3_model, selected_classifier)