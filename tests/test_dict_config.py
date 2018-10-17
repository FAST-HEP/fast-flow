from __future__ import absolute_import
import pytest
import fast_flow.v1.dict_config as dict_config
import os
import sys
sys.path.append(os.path.dirname(__file__))
from . import fake_scribbler_to_test as fakes


def test_get_stage_class_full_module():
    actual_class = dict_config.get_stage_class("fake_scribbler_to_test.FakeScribblerArgs", None, raise_exception=True)
    assert fakes.FakeScribblerArgs.__name__ == actual_class.__name__


def test_get_stage_class_default_module():
    actual_class = dict_config.get_stage_class("FakeScribblerArgs", default_module=fakes, raise_exception=True)
    assert fakes.FakeScribblerArgs.__name__ == actual_class.__name__


def test__make_stage_string():
    name, stage = dict_config._make_stage(1, {"just_a_stage_name": "FakeScribblerArgs"}, default_module=fakes)
    assert stage.__name__, fakes.FakeScribblerArgs.__name__
    assert name == "just_a_stage_name"


@pytest.fixture
def binned_df_cfg():
    return {"my_first_stage": "FakeScribblerArgs"}


@pytest.fixture
def cutflow_cfg():
    return {"my_second_stage": "FakeScribbler"}


def test__make_stage_binned_df(binned_df_cfg):
    name, stage = dict_config._make_stage(2, binned_df_cfg, default_module=fakes)
    assert stage.__name__, fakes.FakeScribblerArgs.__name__
    assert name == "my_first_stage"


def test__make_stage_cutflow(cutflow_cfg):
    name, stage = dict_config._make_stage(2, cutflow_cfg, default_module=fakes)
    assert stage.__name__, fakes.FakeScribbler.__name__
    assert name == "my_second_stage"


def test__make_stage_raises():
    with pytest.raises(dict_config.BadStagesDescription) as ex:
        cfg = {"my_third_stage": "bad_stage_type"}
        dict_config._make_stage(3, cfg)
    assert "Unknown type" in str(ex)

    with pytest.raises(dict_config.BadStagesDescription) as ex:
        cfg = {"my_third_stage": "CutFlow",
               "bad_fourth_stage": "BinnedDataframe"}
        dict_config._make_stage(4, cfg)
    assert "More than one key" in str(ex)


@pytest.fixture
def a_stage_list(binned_df_cfg, cutflow_cfg):
    return [binned_df_cfg, cutflow_cfg]


def test__create_stages(a_stage_list):
    stages = dict_config._create_stages(a_stage_list, default_module=fakes)
    assert len(stages) == 2
    assert stages[0][0] == "my_first_stage"
    assert stages[1][0] == "my_second_stage"
    assert stages[0][1].__name__ == fakes.FakeScribblerArgs.__name__
    assert stages[1][1].__name__ == fakes.FakeScribbler.__name__


@pytest.fixture
def all_stage_configs():
    bins_alpha = {"in": "AlphaT", "out": "alphaT", "bins": dict(nbins=10, low=0, high=2.5)}
    bins_pt = {"in": "jet_pt", "out": "pt_leadJet", "bins": dict(edges=[0, 20., 100.], overflow=True), "index": 0}
    bins_region = {"in": "REGION", "out": "region"}
    weight_dict = dict(none=1, weighted="weight")
    binned_df_cfg_1 = dict(binning=[bins_pt, bins_region], weights=weight_dict)
    binned_df_cfg_2 = dict(binning=[bins_alpha], weights=None)

    selection_cut_1 = "ev.jet_pt[0] > 0"
    selection_cut_2 = "ev.nJet > 1"
    selection = dict(All=[selection_cut_1, dict(Any=dict(Not=selection_cut_2))])
    cutflow_cfg = dict(selection=selection,
                       aliases=dict(some_alias="ev.something == 1"),
                       counter_weights="an_attribrute")
    return dict(my_first_stage=binned_df_cfg_1, my_second_stage=cutflow_cfg, my_third_stage=binned_df_cfg_2)


# def test__configure_stages(a_stage_list, all_stage_configs, tmpdir):
#    stages = dict_config._create_stages(a_stage_list, tmpdir)
#    dict_config._configure_stages(stages, all_stage_configs)
#
#
# def test_sequence_from_dict(a_stage_list, all_stage_configs, tmpdir):
#    rc_pairs = dict_config.sequence_from_dict(a_stage_list, output_dir=str(tmpdir), **all_stage_configs)
#    # 3 stages in list, but one stage makes 2 pairs, so look for 4 rc pairs in total
#    assert len(rc_pairs) == 4
