from __future__ import absolute_import
import six
import importlib
from .config_exceptions import BadConfig
import os
import sys
import logging
logger = logging.getLogger(__name__)


__all__ = ["sequence_from_dict"]


class BadStagesDescription(BadConfig):
    pass


class BadStageList(BadConfig):
    pass


def sequence_from_dict(stages, general={}, **stage_descriptions):
    output_dir = general.get("output_dir", os.getcwd())
    default_module = general.get("backend", None)
    if default_module:
        default_module = importlib.import_module(default_module)
    stages = _create_stages(stages, default_module=default_module)
    stages = _configure_stages(stages, output_dir, stage_descriptions)

    return stages


def _create_stages(stages, default_module=None):
    if not isinstance(stages, list):
        msg = "Bad stage list: Should be a list"
        logger.error(msg + ", but instead got a '{}'".format(type(stages)))
        raise BadStageList(msg)
    return [_make_stage(i, stage_cfg, default_module=default_module) for i, stage_cfg in enumerate(stages)]


def _configure_stages(stages, output_dir, stage_descriptions):
    out_stages = []
    for name, stage_class in stages:
        cfg = stage_descriptions.get(name, None)
        if not cfg:
            raise BadStagesDescription("Missing description for stage '{}'".format(name))
        if isinstance(cfg, dict):
            cfg.setdefault("name", name)
            cfg.setdefault("out_dir", output_dir)
            stage = stage_class(**cfg)
        elif isinstance(cfg, list):
            stage = stage_class(*cfg)
        else:
            stage = stage_class(cfg, name=name)
        out_stages.append(stage)
    return out_stages


def _make_stage(index, stage_cfg, default_type="BinnedDataframe", default_module=None):
    if isinstance(stage_cfg, dict):
        if len(stage_cfg) != 1:
            msg = "More than one key in dictionary spec for stage {} in stages list".format(index)
            logger.error(msg + "\n dictionary given: {}".format(stage_cfg))
            raise BadStagesDescription(msg)
        [(name, stage_type)] = stage_cfg.items()
        if not isinstance(stage_type, six.string_types):
            msg = "Type of stage {} in stages list should be specified as a string".format(index)
            logger.error(msg + "\n Stage Type provided: {}".format(stage_type))
            raise BadStagesDescription(msg)
    else:
        msg = "Bad stage configuration, for stage {} in stages list".format(index)
        logger.error(msg + ". Each stage config must be a dictionary with single key")
        raise BadStagesDescription(msg)

    # Find the actual concrete class based on the string
    stage_class = get_stage_class(stage_type, default_module, raise_exception=False)
    if not stage_class:
        raise BadStagesDescription("Unknown type for stage '{}': {}".format(name, stage_type))
    return (name, stage_class)


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
