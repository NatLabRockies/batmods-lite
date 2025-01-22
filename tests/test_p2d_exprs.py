import pytest
import numpy as np
import bmlite as bm


@pytest.fixture(scope='module')
def sim():
    with pytest.warns(UserWarning):
        sim = bm.P2D.Simulation()
    return sim


@pytest.fixture(scope='module')
def soln(sim):
    sinusoid = lambda t: 3.8 + 10e-3*np.sin(2.*np.pi*t / 15.)  # 10 mV, 15 Hz

    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600., 10.), limits=('voltage_V', 3.))
    expr.add_step('current_A', 0., (600., 10.))
    expr.add_step('current_C', -2., (3600., 10.), limits=('voltage_V', 4.3))
    expr.add_step('voltage_V', 4.3, (600., 10.))
    expr.add_step('power_W', 0.15, (3600., 10.), limits=('voltage_V', 3.8))
    expr.add_step('voltage_V', sinusoid, (60., 1.))

    soln = sim.run(expr)

    return soln


def test_constant_current(soln):
    ccsoln = soln.get_steps(0)
    assert ccsoln.success

    checks = ccsoln._verify()
    assert all(checks.values())


def test_constant_voltage(soln):
    cvsoln = soln.get_steps(3)
    assert cvsoln.success

    checks = cvsoln._verify()
    assert all(checks.values())


def test_constant_power(soln):
    cpsoln = soln.get_steps(4)
    assert cpsoln.success

    checks = cpsoln._verify()
    assert all(checks.values())


def test_dynamic_load(soln):
    dysoln = soln.get_steps(5)
    assert dysoln.success

    checks = dysoln._verify()
    assert all(checks.values())


def test_event_switches(soln):
    assert soln.status.count(2) == 3
