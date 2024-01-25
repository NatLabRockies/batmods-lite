import os, pytest
from pathlib import Path

import bmlite as bm
from ruamel.yaml import YAML
import matplotlib.pyplot as plt


@pytest.fixture(scope='session')
def sim():
    sim = bm.P2D.Simulation()
    return sim


@pytest.fixture(scope='session')
def exp():
    directory = os.path.dirname(__file__) + '/../bmlite/P2D/default_exps/'
    path = Path(directory + 'constant_current.yaml')
    yaml = YAML()

    exp = yaml.load(path)
    return exp


@pytest.fixture(scope='session')
def sol(sim, exp):
    sol = sim.run_CC(exp)
    return sol


@pytest.fixture(scope='session')
def rootsol(sim, exp):
    rootfn = bm.P2D.roots.VLimits(3.7, 4.2)
    nr_rootfns = rootfn.nr_rootfns

    rootsol = sim.run_CC(exp, rootfn=rootfn, nr_rootfns=nr_rootfns)
    return rootsol


def test_classname(sol):
    assert sol.classname == 'CCSolution'


def test_run_CC(sol):
    assert sol.success


def test_onroot(rootsol):
    assert rootsol.success
    assert rootsol.onroot


def test_verify(sol):
    assert sol.verify(True)

    plt.close('all')
