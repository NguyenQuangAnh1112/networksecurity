import sys

from networksecurity.components import data_validation
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    TrainingPipelineConfig,
)
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()

        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logger.info(f"Initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logger.info(f"Data Initiate Completed")

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifact, data_validation_config
        )
        logger.info(f"Initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info(f"Data Validation Completed")

        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(
            data_validation_artifact, data_transformation_config
        )
        logger.info(f"Initiate the data transfomation")
        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )
        logger.info(f"Data Transformation Completed")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
