import pytest
import numpy as np
import bmlite as bm


@pytest.fixture(scope='module')
def sim():
    sim = bm.P2D.Simulation()
    return sim


@pytest.fixture(scope='module')
def sol(sim):
    expr = bm.Experiment()
    expr.add_step('current_C', -2., (1350., 150))
    sol = sim.run(expr)
    return sol


@pytest.fixture(scope='module')
def rootsol(sim):
    expr = bm.Experiment()
    expr.add_step('current_C', -2., (3600., 5.), limits=('voltage_V', 3.))
    rootsol = sim.run(expr)
    return rootsol


def test_run_CC(sol):
    assert sol.success


def test_onroot(rootsol):
    assert rootsol.success
    assert 'events' in rootsol.message[0]


def test_current_units(sim, sol):
    current_A = -2.*sim.bat.cap

    expr = bm.Experiment()
    expr.add_step('current_A', current_A, (1350., 150))
    sol_A = sim.run(expr)

    np.testing.assert_allclose(sol.y, sol_A.y)


# def test_verify(sol):
#     assert sol.verify(True)

#     plt.close('all')
