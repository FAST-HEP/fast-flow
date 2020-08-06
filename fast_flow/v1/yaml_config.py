import os
import copy
from collections import namedtuple, Counter, defaultdict
from .dict_config import infer_stage_name_class


def _load_yaml(filename):
    import yaml
    with open(filename, "r") as infile:
        cfg = yaml.safe_load(infile)
    return cfg


def config_dict_from_yaml(cfg_filename, output_dir=None, backend=None):
    cfg = _load_yaml(cfg_filename)

    this_dir = os.path.dirname(cfg_filename)
    cfg = expand_imports(cfg, this_dir=this_dir)

    # Override the output_dir in the config file if this function is given one
    if "general" not in cfg:
        cfg["general"] = {}
    if output_dir:
        cfg["general"]["output_dir"] = output_dir
    if backend:
        cfg["general"]["backend"] = backend

    return cfg


_StageDescription = namedtuple("_StageDescription", "name type config")


def expand_imports(cfg, this_dir):
    cfg = copy.deepcopy(cfg)
    stages = cfg.pop("stages")
    general = cfg.pop("general", None)

    internal_stage_list = preprocess_imports(stages, cfg, this_dir)
    expanded_cfg = build_config(internal_stage_list)
    if general is not None:
        expanded_cfg["general"] = general
    return expanded_cfg


def preprocess_imports(stages, configs, this_dir):
    expanded_stages = []
    for i, stage_cfg in enumerate(stages):
        name, target = infer_stage_name_class(i, stage_cfg)
        if name != "IMPORT":
            stage = _StageDescription(name, target, configs[name])
            expanded_stages.append(stage)
            continue

        expanded_stages += _handle_import(target.format(this_dir=this_dir))

    return expanded_stages


def _handle_import(cfg_filename):
    cfg = _load_yaml(cfg_filename)
    stages = cfg.pop("stages")
    this_dir = os.path.dirname(cfg_filename)
    return preprocess_imports(stages, cfg, this_dir=this_dir)


def build_config(internal_stage_list):
    # Count the number of unique stage names
    name_counts = Counter(s.name for s in internal_stage_list)
    stages_with_counter = {s for s, c in name_counts.items() if c > 1}

    out_stages = []
    out_config = {}
    stages_seen = defaultdict(int)
    for stage in internal_stage_list:
        name = stage.name
        if name in stages_with_counter:
            name += "." + str(stages_seen[name])
        stages_seen[stage.name] += 1

        out_stages.append({name: stage.type})
        out_config[name] = stage.config

    out_config["stages"] = out_stages
    return out_config
