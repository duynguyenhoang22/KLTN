from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REFERENCE_DATASET = PROJECT_ROOT / "data" / "reference" / "phase1" / "vismishds_phase1_final.csv"
ANNOTATION_DIR = PROJECT_ROOT / "data" / "annotations"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TAXONOMY_PATH = PROJECT_ROOT / "configs" / "taxonomy.json"
SCHEMA_PATH = PROJECT_ROOT / "configs" / "dataset_v2.schema.json"
METADATA_LLM_CONFIG_PATH = PROJECT_ROOT / "configs" / "metadata_llm.json"
