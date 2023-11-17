import interface
from typing import List, Dict, Union

class MicroMinerPipeline(interface.MicroMinerInterface):

    def clone_and_prepare_src_code(self, github_url: str) -> bool:
        raise NotImplementedError("This method must be implemented by the subclass.")

    def execute_phase_1(self, embedding_model: str, ml_model: str, src_code_path: str) -> Dict[str, List[Dict[str, str]]]:
        raise NotImplementedError("This method must be implemented by the subclass.")

    def execute_phase_2(self, phase1_result: Dict[str, List[Dict[str, str]]], phase2_model: str) -> Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]:

        raise NotImplementedError("This method must be implemented by the subclass.")

    def execute_phase_3(self, phase2_result: Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]], phase3_model: str) -> Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]:
        raise NotImplementedError("This method must be implemented by the subclass.")