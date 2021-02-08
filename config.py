import os
import yaml
import shutil
from constants import CONFIG_PATH
from constants import EXAMPLE_CONFIG_PATH

def get_config():
    if not os.path.exists(CONFIG_PATH):
        shutil.copyfile(EXAMPLE_CONFIG_PATH, CONFIG_PATH)
    with open(CONFIG_PATH, "r") as config_file:
        config = yaml.safe_load(config_file)
    return(config)