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

# 3. Data Ingestion related constants
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData" # Tên collection trên MongoDB
DATA_INGESTION_DATABASE_NAME: str = "TRANSACTION_DB"        # Tên Database
DATA_INGESTION_DIR_NAME: str = "data_ingestion"     # Tên thư mục con
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store" # Nơi chứa file raw
DATA_INGESTION_INGESTED_DIR: str = "ingested"       # Nơi chứa train/test
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2  # Tỷ lệ chia test set (20%)