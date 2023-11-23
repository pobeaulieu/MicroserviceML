from pipeline.microminer_pipeline import MicroMinerPipeline
from config.constants import Phase1EmbeddingModel, Phase1ClassifierModel, Phase2EmbeddingModel, Phase2ClusteringModel, Phase3ClusteringModel

# Create interface object with all desired parameters 
pipeline = MicroMinerPipeline(
    embeddings_model_name_phase_1=Phase1EmbeddingModel.codebert.name, 
    classification_model_name_phase_1=Phase1ClassifierModel.svm.name,
    embeddings_model_name_phase_2=Phase2EmbeddingModel.word2vec.name,
    clustering_model_name_phase_2=Phase2ClusteringModel.GirvanNewman.name,
    clustering_model_name_phase_3=Phase3ClusteringModel.custom_cmeans.name,
)

# Call preprocessing step
pipeline.clone_and_prepare_src_code()

# Call Phase 1
result_phase_1 = pipeline.execute_phase_1()
print(result_phase_1)

# Call Phase 2
result_phase_2 = pipeline.execute_phase_2()
print(result_phase_2)

# Call Phase 3
pipeline.execute_phase_3()