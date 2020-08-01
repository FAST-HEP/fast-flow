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
    this_dir = os.path.dirname(cfg_filename)

    cfg = expand_imports(cfg, output_dir=output_dir, this_dir=this_dir,
                         backend=backend)

    return cfg


def expand_imports(cfg, this_dir, output_dir=None, backend=None):
    expanded_stages = []
    expanded_cfg = copy.deepcopy(cfg)
    stages = expanded_cfg.pop("stages")

    for i, stage_cfg in enumerate(stages):
        name, target = infer_stage_name_class(i, stage_cfg)
        if name != "IMPORT":
            expanded_stages.append(stage_cfg)
            continue

        filename = target.format(this_dir=this_dir)
        expanded = config_dict_from_yaml(filename, output_dir=output_dir, backend=backend)
        new_stages, new_cfg = clean_expansion(expanded, target, i)
        expanded_stages += new_stages
        expanded_cfg.update(new_cfg)

    expanded_cfg["stages"] = expanded_stages
    return expanded_cfg


def clean_expansion(cfg, filename, counter):
    cfg.pop("general")

    old_stages = cfg.pop("stages")
    name = "{file}({counter})::{stage}"
    new_stages = []
    for i, stage_cfg in enumerate(old_stages):
        old_name, target = infer_stage_name_class(i, stage_cfg)
        new_name = name.format(file=filename,counter=counter,stage=old_name)
        new_stages.append({new_name: target})
        cfg[new_name] = cfg.pop(old_name)

    return new_stages, cfg
