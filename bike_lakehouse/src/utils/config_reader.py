import os
import yaml




def get_project_root():

    current_path = os.getcwd()

    # remove /src/utils if running from utils folder
    project_root = os.path.dirname(
        os.path.dirname(current_path)
    )

    return project_root



base_path = get_project_root()

def read_config(environment):
    with open(f"{base_path}/config/{environment}/config.yaml","r") as f:
        config = yaml.safe_load(f)

    return config