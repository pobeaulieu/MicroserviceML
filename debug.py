from pipeline.microminer_pipeline import MicroMinerPipeline

# Create interface object with all desired parameters 
pipeline = MicroMinerPipeline()

# Call Phase 1
pipeline.execute_phase_1()
print(pipeline.num_clusters)