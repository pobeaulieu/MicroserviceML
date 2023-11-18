from pipeline.microminer_pipeline import MicroMinerPipeline
from config.constants import Phase1Model, Phase1ClassifierModel, Phase2Model

# Create interface object with all desired parameters 
pipeline = MicroMinerPipeline(
    embeddings_model_name_phase_1=Phase1Model.codebert.name, 
    classification_model_name_phase_1=Phase1ClassifierModel.knn.name,
    clustering_model_name_phase_2=Phase2Model.Louvain
)

# Call Phase 1
result_phase_1 = pipeline.execute_phase_1()
print(result_phase_1)

# Call Phase 2
pipeline.execute_phase_2()