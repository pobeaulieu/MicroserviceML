import interface
from typing import List, Dict, Union

class MockImplementation(interface.MicroMinerInterface):
    def clone_and_prepare_src_code(self) -> bool:
        # print(f"Mock: Cloning and preparing source code from {github_url}")
        # Simulate successful operation
        return True

    def execute_phase_1(self) -> Dict[str, List[Dict[str, str]]]:
        # print(f"Mock: Executing Phase 1 with embedding_model={embedding_model}, ml_model={ml_model}, src_code_path={src_code_path}")
        # Simulate phase 1 result
        return {
            "applicationClasses": [
                {"className": "x"},
                {"className": "x"}
            ]
        }

    def execute_phase_2(self) -> Dict[str, Union[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]]:
        # print(f"Mock: Executing Phase 2 with phase1_result={phase1_result}, phase2_model={phase2_model}")
        # Simulate phase 2 result
        return {
            "applicationServices": {
                "service": [
                    {"className": "x"},
                    {"className": "x"}
                ],
                "service": [
                    {"className": "x"},
                    {"className": "x"}
                ]
            },
            "utilityServices": {
                "service": [
                    {"className": "x"},
                    {"className": "x"}
                ]
            },
            "entityServices": {
                "service": [
                    {"className": "x"},
                    {"className": "x"}
                ]
            }
        }

    def execute_phase_3(self) -> Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]:
        # print(f"Mock: Executing Phase 3 with phase2_result={phase2_result}, phase3_model={phase3_model}")
        # Simulate phase 3 result
        return {
            "microservices": {
                "microservice": {
                    "applicationServices": {
                        "service": [
                            {"className": "x"},
                            {"className": "x"}
                        ],
                        "service": [
                            {"className": "x"},
                            {"className": "x"}
                        ]
                    },
                    "utilityServices": {
                        "service": [
                            {"className": "x"},
                            {"className": "x"}
                        ]
                    },
                    "entityServices": {
                        "service": [
                            {"className": "x"},
                            {"className": "x"}
                        ]
                    }
                }
            }
        }

# Example Usage:
# mock_impl = MockImplementation()
# mock_impl.clone_and_prepare_src_code("https://github.com/example/repo")
# phase1_result = mock_impl.execute_phase_1("embedding_model", "ml_model", "/path/to/src/code")
# phase2_result = mock_impl.execute_phase_2(phase1_result, "phase2_model")
# phase3_result = mock_impl.execute_phase_3(phase2_result, "phase3_model")
