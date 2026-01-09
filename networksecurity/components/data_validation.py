from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.logging.logger import logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml, write_yaml

from scipy.stats import ks_2samp
import pandas as pd
import os, sys

"""
🔄 Workflow hoàn chỉnh

    DataIngestionArtifact
             ↓
    (train.csv, test.csv)
             ↓
      Data Validation
             ↓
    ┌────────┴────────┐
Kiểm tra cột     Detect Drift
    │                 │
    └────────┬────────┘
             ↓
    validation_status: True/False
    drift_report.json
             ↓
  DataValidationArtifact
"""


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):

        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            logger.info(f"Required number of columns: {number_of_columns}")
            logger.info(f"Data Frame len columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def is_numerical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            set_columns_df = set(dataframe.columns)
            set_columns_schema = set(list(self._schema_config.numerical_columns))

            intersection = set_columns_df.intersection(set_columns_schema)
            check = len(intersection) == len(set_columns_schema)

            if not check:
                missing_cols = set_columns_schema - set_columns_df
                logger.error(f"Missing {missing_cols} columns")

            if len(set_columns_df) > len(set_columns_schema):
                excess_cols = set_columns_df - set_columns_schema
                logger.warning(f"Exceeding {excess_cols} columns")

            return check

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                _, p_value = ks_2samp(d1, d2)
                if p_value >= threshold:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update(
                    {
                        col: {
                            "p_value": float(p_value),
                            "drift_status": is_found,
                        }
                    }
                )
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            drift_path = os.path.dirname(drift_report_file_path)
            os.makedirs(drift_path, exist_ok=True)
            write_yaml(drift_report_file_path, report)

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read the data from train and test
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # validate number of columns
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain all columns.\n"
                logger.error(error_message)

            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contain all columns.\n"
                logger.error(error_message)

            # check numerical columns exist
            status = self.is_numerical_columns_exist(train_dataframe)
            if not status:
                error_message = (
                    f"Train dataframe does not contain all numerical columns.\n"
                )
                logger.error(error_message)

            status = self.is_numerical_columns_exist(test_dataframe)
            if not status:
                error_message = (
                    f"Test dataframe does not contain all numerical columns.\n"
                )
                logger.error(error_message)

            # check data drift
            validation_status = self.detect_dataset_drift(
                base_df=train_dataframe, current_df=test_dataframe
            )

            # create directories for valid and invalid data
            os.makedirs(self.data_validation_config.valid_data_dir, exist_ok=True)
            os.makedirs(self.data_validation_config.invalid_data_dir, exist_ok=True)

            # Always save to valid directory so pipeline can continue
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False
            )
            
            if validation_status:
                logger.info("Data validation passed. Data saved to valid directory.")
            else:
                # Also save to invalid directory for tracking drift issues
                train_dataframe.to_csv(
                    self.data_validation_config.invalid_train_file_path, index=False
                )
                test_dataframe.to_csv(
                    self.data_validation_config.invalid_test_file_path, index=False
                )
                logger.warning(
                    "Data drift detected! Data saved to both valid and invalid directories."
                )

            # create and return DataValidationArtifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logger.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
