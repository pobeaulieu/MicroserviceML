from typing import List, Dict, Union

class MicroMinerInterface:
    def clone_and_prepare_src_code(self, github_url: str) -> bool:
        """
        Clones and prepares source code from a GitHub repository.

        Parameters:
        - github_url (str): GitHub URL to the repository.

        Returns:
        - bool: True if successful, False otherwise.
        """
        raise NotImplementedError("This method must be implemented by the subclass.")

    def execute_phase_1(self, embedding_model: str, ml_model: str, src_code_path: str) -> Dict[str, List[Dict[str, str]]]:
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

    def execute_phase_2(self, phase1_result: Dict[str, List[Dict[str, str]]], phase2_model: str) -> Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]:
        """
        Executes Phase 2 of the process.

        Parameters:
        - phase1_result (Dict[str, List[Dict[str, str]]]): JSON returned from execute_phase_1.
        - phase2_model (str): Enum representing the Phase 2 model.

        Returns:
        - Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]: JSON format with application, utility, and entity services.
        """
        raise NotImplementedError("This method must be implemented by the subclass.")

    def execute_phase_3(self, phase2_result: Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]], phase3_model: str) -> Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]:
        """
        Executes Phase 3 of the process.

        Parameters:
        - phase2_result (Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]): JSON returned from execute_phase_2.
        - phase3_model (str): Enum representing the Phase 3 model.

        Returns:
        - Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]: JSON format with microservices and their services.
        """
        raise NotImplementedError("This method must be implemented by the subclass.")

