import os


def config_dict_from_yaml(cfg_filename, output_dir=None, backend=None):
    import yaml
    with open(cfg_filename, "r") as infile:
        cfg = yaml.safe_load(infile)

    # Override the output_dir in the config file if this function is given one
    if "general" not in cfg:
        cfg["general"] = {}
    if output_dir:
        cfg["general"]["output_dir"] = output_dir
    if backend:
        cfg["general"]["backend"] = backend
    cfg["general"]["this_dir"] = os.path.dirname(cfg_filename)

    return cfg
