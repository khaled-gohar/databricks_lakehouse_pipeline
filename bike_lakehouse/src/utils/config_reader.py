import yaml



def read_config(base_path,environment):
    with open(f"{base_path}/{environment}/config.yaml","r") as f:
        config = yaml.safe_load(f)

    return config