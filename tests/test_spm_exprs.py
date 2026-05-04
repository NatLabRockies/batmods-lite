import pytest
import numpy as np
import bmlite as bm


@pytest.fixture(scope='module')
def sim():
    with pytest.warns(UserWarning):
        sim = bm.SPM.Simulation()
    return sim


@pytest.fixture(scope='module')
def soln(sim):
    sinusoid = lambda t: 3.8 + 10e-3*np.sin(2.*np.pi*t / 15.)  # 10 mV, 15 Hz

    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600., 10.), limits=('voltage_V', 3.8))
    expr.add_step('current_A', 0., (300., 10.))
    expr.add_step('current_C', -2., (3600., 10.), limits=('voltage_V', 4.3))
    expr.add_step('voltage_V', 4.3, (300., 10.))
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


def test_capacity_limit(sim):
    # Voltage limit experiment
    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600., 10.), limits=('voltage_V', 3.8))
    soln_volt = sim.run(expr)
    iA_v = soln_volt.vars["current_A"]
    ts_v = soln_volt.vars["time_s"]
    th_v = soln_volt.vars["time_h"]
    phiV_v = soln_volt.vars["voltage_V"]

    # Compute capacity used
    from scipy import integrate
    capacity_lim = integrate.trapezoid(iA_v, th_v)

    # Capacity limit experiment
    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600., 10.), limits=('capacity_Ah', capacity_lim))
    soln_cap = sim.run(expr)
    ts_cap = soln_cap.vars["time_s"]
    phiV_cap = soln_cap.vars["voltage_V"]

    # Make sure sim ran for the same time
    end_t_v = ts_v[-1]
    end_t_cap = ts_cap[-1]
    assert abs(end_t_v - end_t_cap)/end_t_v < 1e-12
 
    # Make sure gave the same output
    t_interp = np.linspace(max(ts_v.min(), ts_cap.min()), min(ts_v.max(), ts_cap.max()), 100)
    phiV_v_int = np.interp(t_interp, ts_v, phiV_v)
    phiV_cap_int = np.interp(t_interp, ts_cap, phiV_cap)
    assert np.mean(abs(phiV_v_int - phiV_cap_int)) < 1e-12

    # Wrong capacity limit experiment
    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600., 10.), limits=('capacity_Ah', capacity_lim/2))
    soln_cap = sim.run(expr)
    ts_cap = soln_cap.vars["time_s"]

    # Make sure sim ran for different time
    end_t_cap = ts_cap[-1]
    assert abs(end_t_v - end_t_cap)/end_t_v > 1e-12


    return soln

