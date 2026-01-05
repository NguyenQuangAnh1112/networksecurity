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
