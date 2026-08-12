import os

DATASET_PATH = '/content/data/dataset.csv'
CLEAN_TEXT_COLUMN = 'texto_completo'
TARGET_COLUMN = 'categoria'

# Model training configuration
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Model saving path
MODELS_DIR = '/content/models'
MODEL_PATH0 = os.path.join(MODELS_DIR, 'pipeline_techmind.pkl')
MODEL_PATH = os.path.join(MODELS_DIR, 'optimized_pipeline_techmind.pkl')


# Metrics saving path
REPORTS_DIR = '/content/reports' # Changed from METRICS_DIR to REPORTS_DIR
METRICS_PATH0 = os.path.join(REPORTS_DIR, 'metrics.json')
CONFUSION_MATRIX_PATH0 = os.path.join(REPORTS_DIR, 'confusion_matrix.png')

METRICS_PATH = os.path.join(REPORTS_DIR, 'optimization_metrics.json')
CONFUSION_MATRIX_PATH = os.path.join(REPORTS_DIR, 'optimization_confusion_matrix.png')

# Ensure directories exist
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR, exist_ok=True)
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR, exist_ok=True) # Ensure REPORTS_DIR exists
