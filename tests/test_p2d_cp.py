import os, pytest
from pathlib import Path

import numpy as np
import bmlite as bm
from ruamel.yaml import YAML
import matplotlib.pyplot as plt


@pytest.fixture(scope='module')
def sim():
    sim = bm.P2D.Simulation()
    return sim


@pytest.fixture(scope='module')
def exp():
    directory = os.path.dirname(__file__) + '/../bmlite/P2D/default_exps/'
    path = Path(directory + 'constant_power.yaml')
    yaml = YAML()

    exp = yaml.load(path)
    return exp


@pytest.fixture(scope='module')
def sol(sim, exp):
    sol = sim.run_CP(exp)
    return sol


@pytest.fixture(scope='module')
def rootsol(sim, exp):
    rootfn = bm.P2D.roots.VLimits(3.7, np.nan)
    rootsol = sim.run_CP(exp, rootfn=rootfn, nr_rootfns=rootfn.size)
    return rootsol


def test_classname(sol):
    assert sol.classname == 'CPSolution'


def test_run_CP(sol):
    assert sol.success


def test_onroot(rootsol):
    assert rootsol.success
    assert rootsol.onroot


def test_verify(sol):
    assert sol.verify(True)

    plt.close('all')
