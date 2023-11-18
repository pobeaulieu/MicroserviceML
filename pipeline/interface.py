from typing import List, Dict, Union
from config.constants import Phase1Model, Phase1ClassifierModel, Phase2EmbeddingsModel, Phase2Model, Phase3Model

class MicroMinerInterface:

    def __init__(self, github_url: str = None, embeddings_model_name_phase_1: Phase1Model = None, classification_model_name_phase_1: Phase1ClassifierModel = None, clustering_model_name_phase_2: Phase2Model = None, embeddings_model_name_phase_2: Phase2EmbeddingsModel = None, call_graph: str = None, clustering_model_name_phase_3: Phase3Model = None, num_clusters: int = -1, max_d: int = -1):
        self.github_url = github_url
        
        # Phase 1 parameters
        self.embeddings_model_name_phase_1 = embeddings_model_name_phase_1
        self.classification_model_name_phase_1 = classification_model_name_phase_1
        self.embeddings_phase_1 = {}

        # Phase 2 parameters
        self.clustering_model_name_phase_2 = clustering_model_name_phase_2
        self.embeddings_model_name_phase_2 = embeddings_model_name_phase_2
        self.call_graph = call_graph
        self.embeddings_phase_2 = {}
        self.communities = {}
        self.class_graph = {}

        # Phase 3 parameters
        self.clustering_model_name_phase_3 = clustering_model_name_phase_3
        self.num_clusters = num_clusters
        self.max_d = max_d
        self.service_graph = {}


    def clone_and_prepare_src_code(self) -> bool:
        """
        Clones and prepares source code from a GitHub repository.

        Parameters:
        - github_url (str): GitHub URL to the repository.

        Returns:
        - bool: True if successful, False otherwise.
        """
        raise NotImplementedError("This method must be implemented by the subclass.")

    def execute_phase_1(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Executes Phase 1 of the process.

        Parameters:
        - embedding_model (str): Enum representing the embedding model.
        - ml_model (str): Enum representing the ML model.
        - src_code_path (str): Path to the monolith source code.

        Returns:
        - Dict[str, List[Dict[str, str]]]: JSON format with application classes.
        """
        raise NotImplementedError("This method must be implemented by the subclass.")

    def execute_phase_2(self) -> Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]:
        """
        Executes Phase 2 of the process.

        Parameters:
        - phase1_result (Dict[str, List[Dict[str, str]]]): JSON returned from execute_phase_1.
        - phase2_model (str): Enum representing the Phase 2 model.

        Returns:
        - Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]: JSON format with application, utility, and entity services.
        """
        raise NotImplementedError("This method must be implemented by the subclass.")

    def execute_phase_3(self) -> Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]:
        """
        Executes Phase 3 of the process.

        Parameters:
        - phase2_result (Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]): JSON returned from execute_phase_2.
        - phase3_model (str): Enum representing the Phase 3 model.

        Returns:
        - Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]: JSON format with microservices and their services.
        """
        raise NotImplementedError("This method must be implemented by the subclass.")

