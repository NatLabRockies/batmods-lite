import pytest
import bmlite as bm


@pytest.fixture(scope='module')
def sim():
    sim = bm.P2D.Simulation()
    return sim


@pytest.fixture(scope='module')
def sol(sim):
    expr = bm.Experiment()
    expr.add_step('power_W', -0.15, (1350., 150))
    sol = sim.run(expr)
    return sol


@pytest.fixture(scope='module')
def rootsol(sim):
    expr = bm.Experiment()
    expr.add_step('power_W', -0.15, (3600., 5.), limits=('voltage_V', 3.7))
    rootsol = sim.run(expr)
    return rootsol


def test_run_CP(sol):
    assert sol.success


def test_onroot(rootsol):
    assert rootsol.success
    assert 'events' in rootsol.message[0]


# def test_verify(sol):
#     assert sol.verify(True)

#     plt.close('all')
