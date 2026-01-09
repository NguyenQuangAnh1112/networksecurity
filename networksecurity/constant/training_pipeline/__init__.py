import os
import sys
import numpy as np
import pandas as pd


# 1. Các hằng số định danh chung
TARGET_COLUMN = "Result"
PIPELINE_NAME = "NetworkSecurity"
ARTIFACT_DIR = "Artifacts"
FILE_NAME = "phishing_data.csv"

# 2. Các hằng số định danh file dữ liệu
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

# 3. Data Ingestion related constants
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"  # Tên collection trên MongoDB
DATA_INGESTION_DATABASE_NAME: str = "TRANSACTION_DB"  # Tên Database
DATA_INGESTION_DIR_NAME: str = "data_ingestion"  # Tên thư mục con
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"  # Nơi chứa file raw
DATA_INGESTION_INGESTED_DIR: str = "ingested"  # Nơi chứa train/test
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2  # Tỷ lệ chia test set (20%)

# 4. Data Validation related constants
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPOR_FILE_NAME: str = "report.yaml"

# 5. Data Transformation related constants
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}
