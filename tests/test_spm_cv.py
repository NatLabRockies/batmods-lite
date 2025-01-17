import pytest
import bmlite as bm


@pytest.fixture(scope='module')
def sim():
    sim = bm.SPM.Simulation()
    return sim


@pytest.fixture(scope='module')
def sol(sim):
    expr = bm.Experiment()
    expr.add_step('voltage_V', 4.0, (1350., 150))
    sol = sim.run(expr)
    return sol


@pytest.fixture(scope='module')
def rootsol(sim):
    expr = bm.Experiment()
    expr.add_step('voltage_V', 4.0, (1350., 150), limits=('current_C', -0.25))
    rootsol = sim.run(expr)
    return rootsol


def test_run_CV(sol):
    assert sol.success


def test_onroot(rootsol):
    assert rootsol.success
    assert 'events' in rootsol.message[0]


# def test_verify(sol):
#     assert sol.verify(True)

#     plt.close('all')
