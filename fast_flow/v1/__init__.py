from __future__ import absolute_import
from .dict_config import sequence_from_dict


__all__ = ["read_sequence_yaml", "read_sequence_dict"]


def read_sequence_yaml(cfg_filename, output_dir=None):
    import yaml
    with open(cfg_filename, "r") as infile:
        cfg = yaml.load(infile)

    # Override the output_dir in the config file if this function is given one
    if output_dir:
        if "general" not in cfg:
            cfg["general"] = {}
        cfg["general"]["output_dir"] = output_dir

    return sequence_from_dict(**cfg)


def read_sequence_dict(cfg):
    return sequence_from_dict(**cfg)
