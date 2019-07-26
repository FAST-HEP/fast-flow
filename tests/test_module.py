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
    out_file = tmpdir / "config.yml"
    out_file.write(content)
    return out_file


def test_read_sequence_yaml(config_1):
    stages = fast_flow.read_sequence_yaml(config_1)
    assert len(stages) == 2
    assert isinstance(stages[0], fakes.FakeScribbler)
    assert isinstance(stages[1], fakes.FakeScribblerArgs)
    assert stages[1].an_int == 3
    assert stages[1].a_str == "hello world"
    assert len(stages[1].other_args) == 2


def test_compile_sequence_yaml(config_1):
    stages = fast_flow.compile_sequence_yaml(config_1)
    stages = stages()
    assert len(stages) == 2
    assert isinstance(stages[0], fakes.FakeScribbler)
    assert isinstance(stages[1], fakes.FakeScribblerArgs)
    assert stages[1].an_int == 3
    assert stages[1].a_str == "hello world"
    assert len(stages[1].other_args) == 2
