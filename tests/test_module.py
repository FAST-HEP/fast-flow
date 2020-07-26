from __future__ import absolute_import
import pytest
import fast_flow.v1 as fast_flow
from . import fake_scribbler_to_test as fakes


@pytest.fixture
def config_1(tmpdir):
    content = """
    general:
        backend: tests.fake_scribbler_to_test
        output_dir: %(tmpdir)s

    stages:
        - my_first_stage: tests.fake_scribbler_to_test.FakeScribbler
        - my_second_stage: FakeScribblerArgs

    my_first_stage: {}
    my_second_stage:
        an_int: 3
        a_str: hello world
        some_other_arg: True
        yet_more_arg: [0, 1, 2]
    """ % dict(tmpdir=str(tmpdir))
    out_file = tmpdir / "config_1.yml"
    out_file.write(content)
    return out_file


@pytest.fixture
def config_2(config_1, tmpdir):
    subdir = tmpdir / "subdir"
    subdir.mkdir()
    subsubdir = subdir / "subsubdir"
    subsubdir.mkdir()

    content = """
    stages:
        - IMPORT: "{this_dir}/config_1.yml"
        - my_third_stage: FakeScribblerArgs

    my_third_stage:
        an_int: 100
        a_str: wooorrrddd
        yet_more_arg:
            one: 1
            two: "222"
    """
    config_2 = tmpdir / "config_2.yml"
    config_2.write(content)

    content = """
    stages:
        - IMPORT: "{this_dir}/../config_2.yml"
    """
    config_3 = subdir / "config_3.yml"
    config_3.write(content)

    content = """
    stages:
        - IMPORT: "{this_dir}/subdir/config_3.yml"
    """
    config_4 = tmpdir / "config_4.yml"
    config_4.write(content)

    content = """
    stages:
        - IMPORT: "{this_dir}/../../config_4.yml"
    """
    config_5 = subsubdir / "config_5.yml"
    config_5.write(content)
    return config_5


def test_read_sequence_yaml(config_1):
    stages = fast_flow.read_sequence_yaml(str(config_1))
    assert len(stages) == 2
    assert isinstance(stages[0], fakes.FakeScribbler)
    assert isinstance(stages[1], fakes.FakeScribblerArgs)
    assert stages[1].an_int == 3
    assert stages[1].a_str == "hello world"
    assert len(stages[1].other_args) == 2


def test_compile_sequence_yaml(config_1):
    stages = fast_flow.compile_sequence_yaml(str(config_1))
    stages = stages()
    assert len(stages) == 2
    assert isinstance(stages[0], fakes.FakeScribbler)
    assert isinstance(stages[1], fakes.FakeScribblerArgs)
    assert stages[1].an_int == 3
    assert stages[1].a_str == "hello world"
    assert len(stages[1].other_args) == 2


def test_read_sequence_yaml_import(config_2, tmpdir):
    stages = fast_flow.compile_sequence_yaml(str(config_2), backend=fakes)
    stages = stages()
    assert len(stages) == 3
    assert isinstance(stages[0], fakes.FakeScribbler)
    assert isinstance(stages[1], fakes.FakeScribblerArgs)
    assert stages[1].an_int == 3
    assert stages[1].a_str == "hello world"
    assert isinstance(stages[2], fakes.FakeScribblerArgs)
    assert stages[2].an_int == 100
    assert stages[2].a_str == "wooorrrddd"
    assert len(stages[2].other_args) == 1
