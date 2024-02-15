import pytest

import bmlite as bm
import matplotlib.pyplot as plt


@pytest.fixture(scope='module')
def sim():
    sim = bm.P2D.Simulation()
    return sim


def test_simulation(sim):
    assert sim


def test_fake_yaml():
    with pytest.raises(FileNotFoundError):
        sim = bm.SPM.Simulation('fake.yaml')


def test_j_pattern(sim):
    lband, uband = sim.j_pattern()
    assert sim.lband == lband
    assert sim.uband == uband

    plt.close('all')


def test_copy(sim):
    sim2 = sim.copy()
    assert all(sim2.sv_0 == sim.sv_0)


def test_templates():
    bm.P2D.templates()
    bm.P2D.templates(0)
    bm.P2D.templates('graphite_nmc532')
    bm.P2D.templates('graphite_nmc532.yaml')
    bm.P2D.templates(exp=0)
    bm.P2D.templates(exp='constant_current')
    bm.P2D.templates(exp='constant_current.yaml')
    assert True
