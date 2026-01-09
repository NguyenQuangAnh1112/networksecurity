import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import os, sys
import numpy as np
import dill
import pickle
from box.exceptions import BoxValueError
from box import ConfigBox


def read_yaml(path_to_yaml: str) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


def write_yaml(path_to_yaml: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(path_to_yaml):
                os.remove(path_to_yaml)
        os.makedirs(os.path.dirname(path_to_yaml), exist_ok=True)
        with open(path_to_yaml, "w") as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    try:
        logger.info(f"Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logger.info(f"Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
