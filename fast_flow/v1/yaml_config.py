import os
import copy
from .dict_config import infer_stage_name_class


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

    cfg = expand_imports(cfg, output_dir=output_dir, backend=backend)

    return cfg


def expand_imports(cfg, output_dir=None, backend=None):
    expanded_stages = []
    expanded_cfg = copy.deepcopy(cfg)
    stages = expanded_cfg.pop("stages")
    this_dir = expanded_cfg["general"]["this_dir"]

    for i, stage_cfg in enumerate(stages):
        name, target = infer_stage_name_class(i, stage_cfg)
        if name == "IMPORT":
            target = target.format(this_dir=this_dir)
            expanded = config_dict_from_yaml(target, output_dir=output_dir, backend=backend)
            expanded_stages += expanded.pop("stages")
            # TODO: Add check that imported satages dont overwrite existing ones
            expanded_cfg.update(expanded)
            continue
        if name in expanded_stages:
            raise ValueError("Repeated stage name: '%s'" % name)
        expanded_stages.append(stage_cfg)
    expanded_cfg["stages"] = expanded_stages
    return expanded_cfg
