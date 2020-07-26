from __future__ import absolute_import
from .dict_config import read_sequence_dict, compile_sequence_dict
from .yaml_config import config_dict_from_yaml


__all__ = ["read_sequence_yaml", "compile_sequence_yaml",
           "read_sequence_dict", "compile_sequence_dict"]


def read_sequence_yaml(cfg_filename, output_dir=None, backend=None, return_cfg=False):
    cfg = config_dict_from_yaml(cfg_filename,
                                output_dir=output_dir,
                                backend=backend)
    sequence = read_sequence_dict(**cfg)
    if return_cfg:
        return sequence, cfg
    return sequence


def compile_sequence_yaml(cfg_filename, output_dir=None, backend=None, return_cfg=False):
    cfg = config_dict_from_yaml(cfg_filename,
                                output_dir=output_dir,
                                backend=backend)
    sequence = compile_sequence_dict(**cfg)
    if return_cfg:
        return sequence, cfg
    return sequence
