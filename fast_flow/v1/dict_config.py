from __future__ import absolute_import
import os
import sys
import logging
import six
import importlib
import copy
from .config_exceptions import BadConfig
from .yaml_config import config_dict_from_yaml
logger = logging.getLogger(__name__)


__all__ = ["read_sequence_dict"]


class BadStagesDescription(BadConfig):
    pass


class BadStageList(BadConfig):
    pass


def read_sequence_dict(stages, general={}, **stage_descriptions):
    return read_sequence_dict_internal(stages, general,
                                       stage_descriptions,
                                       return_future=False)


def compile_sequence_dict(stages, general={}, **stage_descriptions):
    sequence = read_sequence_dict_internal(stages, general,
                                           stage_descriptions,
                                           return_future=True)

    def build():
        return [s() for s in sequence]

    return build


def read_sequence_dict_internal(stages, general={},
                                stage_descriptions={},
                                return_future=False):
    output_dir = general.get("output_dir", os.getcwd())
    default_module = general.get("backend", None)
    if default_module and isinstance(default_module, six.string_types):
        default_module = importlib.import_module(default_module)
    stages = _create_stages(stages, output_dir, stage_descriptions,
                            this_dir=general.get("this_dir", None),
                            default_module=default_module,
                            return_future=return_future)
    return stages


def _create_stages(stages, output_dir, stage_descriptions,
                   this_dir=None, default_module=None, return_future=False):
    if not isinstance(stages, list):
        msg = "Bad stage list: Should be a list"
        logger.error(msg + ", but instead got a '{}'".format(type(stages)))
        raise BadStageList(msg)
    out_stages = []
    for i, stage_cfg in enumerate(stages):
        name, stage_type = infer_stage_name_class(i, stage_cfg)
        if name == "IMPORT":
            out_stages += import_yaml(stage_type, output_dir, this_dir,
                                      return_future=return_future,
                                      default_module=default_module)
            continue

        out_stages += instantiate_stage(name, stage_type, output_dir,
                                        stage_descriptions=stage_descriptions,
                                        default_module=default_module,
                                        return_future=return_future,
                                        )
    return out_stages


def import_yaml(filepath, output_dir, this_dir,
                return_future=False, default_module=None):
    filepath = filepath.format(this_dir=this_dir)
    cfg = config_dict_from_yaml(filepath, output_dir=output_dir, backend=default_module)
    stages = cfg.pop("stages")
    general = cfg.pop("general", {})
    return read_sequence_dict_internal(stages, general,
                                       stage_descriptions=cfg,
                                       return_future=return_future)


def instantiate_stage(name, stage_type, output_dir, stage_descriptions,
                      default_module=None, return_future=False):
    stage_class = get_stage_class(stage_type, default_module, raise_exception=False)
    if not stage_class:
        raise BadStagesDescription("Unknown type for stage '{}': {}".format(name, stage_type))
    result = _configure_stage(name, stage_class, output_dir,
                              stage_descriptions, return_future=return_future)
    return [result]


def _configure_stage(name, stage_class, out_dir,
                     stage_descriptions, return_future=False):
    cfg = stage_descriptions.get(name, None)
    cfg = copy.deepcopy(cfg)
    if cfg is None:
        raise BadStagesDescription("Missing description for stage '{}'".format(name))

    def stage():
        if isinstance(cfg, dict):
            cfg.setdefault("name", name)
            cfg.setdefault("out_dir", out_dir)
            return stage_class(**cfg)
        elif isinstance(cfg, list):
            return stage_class(*cfg)
        else:
            return stage_class(cfg, name=name)

    if return_future:
        return stage
    return stage()


def infer_stage_name_class(index, stage_cfg):
    if not isinstance(stage_cfg, dict):
        msg = "Bad stage configuration, for stage {} in stages list".format(index)
        logger.error(msg + ". Each stage config must be a dictionary with single key")
        raise BadStagesDescription(msg)
    if len(stage_cfg) != 1:
        msg = "More than one key in dictionary spec for stage {} in stages list".format(index)
        logger.error(msg + "\n dictionary given: {}".format(stage_cfg))
        raise BadStagesDescription(msg)
    [(name, stage_type)] = stage_cfg.items()
    if not isinstance(stage_type, six.string_types):
        msg = "Type of stage {} in stages list should be specified as a string".format(index)
        logger.error(msg + "\n Stage Type provided: {}".format(stage_type))
        raise BadStagesDescription(msg)
    return name, stage_type


def get_stage_class(class_name, default_module, raise_exception=True):
    if not default_module:
        default_module = sys.modules[__name__]

    if "." not in class_name:
        module = default_module
    else:
        path = class_name.split(".")
        mod_name = ".".join(path[:-1])
        class_name = path[-1]
        module = importlib.import_module(mod_name)
    actual_class = getattr(module, class_name, None)
    if not actual_class and raise_exception:
        raise RuntimeError("Unknown manip class, '{}'".format(class_name))
    return actual_class
