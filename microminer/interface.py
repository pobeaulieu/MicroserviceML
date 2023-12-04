from typing import List, Dict, Union
import uuid
import pandas as pd
from datetime import datetime
from microminer.config.enums import Phase1EmbeddingModel, Phase1ClassifierModel, Phase2EmbeddingModel, Phase2ClusteringModel, Phase3ClusteringModel

class MicroMinerInterface:

    def __init__(self, 
                 github_url: str = None,
                 path_to_call_graph: str = None, 
                 embeddings_model_name_phase_1: Phase1EmbeddingModel = None, 
                 classification_model_name_phase_1: Phase1ClassifierModel = None, 
                 clustering_model_name_phase_2: Phase2ClusteringModel = None, 
                 embeddings_model_name_phase_2: Phase2EmbeddingModel = None, 
                 alpha_phase_2: float = 0.5,
                 clustering_model_name_phase_3: Phase3ClusteringModel = None, 
                 num_clusters: int = -1, 
                 max_d: int = -1,
                 alpha_phase_3: float = 0.5,
                 training_system_names: List[str] = ["pos", "jforum", "petclinic", "cargotracker"],
                 version: str = 'v_team'):

        
        self.run_id = str(uuid.uuid4())
        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        self.github_url = github_url
        self.path_to_call_graph = path_to_call_graph
        
        # Phase 1 parameters
        self.embeddings_model_name_phase_1 = embeddings_model_name_phase_1
        self.classification_model_name_phase_1 = classification_model_name_phase_1
        self.embeddings_phase_1 = {}
        self.labels = {}

        # Phase 2 parameters
        self.clustering_model_name_phase_2 = clustering_model_name_phase_2
        self.embeddings_model_name_phase_2 = embeddings_model_name_phase_2
        self.embeddings_phase_2 = {}
        self.alpha_phase_2 = alpha_phase_2
        self.normalized_static_distances_between_classes = pd.DataFrame()
        self.normalized_semantic_distances_between_classes = pd.DataFrame()
        self.communities = {}

        # Phase 3 parameters
        self.clustering_model_name_phase_3 = clustering_model_name_phase_3
        self.num_clusters = num_clusters
        self.max_d = max_d
        self.alpha_phase_3 = alpha_phase_3
        self.num_classes = 0

        # Training parameters
        self.version = version
        self.training_system_names = training_system_names

        # Results
        self.result_phase_1 = {}
        self.result_phase_2 = {}
        self.result_phase_3 = {}

    def __str__(self) -> str:
        return (
            f"GitHub URL: {self.github_url}\n"
            f"Phase 1 - Embeddings Model: {self.embeddings_model_name_phase_1}\n"
            f"Phase 1 - Classification Model: {self.classification_model_name_phase_1}\n"
            f"Phase 2 - Clustering Model: {self.clustering_model_name_phase_2}\n"
            f"Phase 2 - Embeddings Model: {self.embeddings_model_name_phase_2}\n"
            f"Phase 2 - Call Graph: {self.call_graph}\n"
            f"Phase 3 - Clustering Model: {self.clustering_model_name_phase_3}\n"
            f"Phase 3 - Number of Clusters: {self.num_clusters}\n"
            f"Phase 3 - Max Distance: {self.max_d}\n"
    )
    
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

