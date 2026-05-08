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
    expr.add_step('current_C', 2., (3600., 10),
                  limits=('voltage_V', 3.8))
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
    expr.add_step('current_C', 2., (3600., 10.),
                  limits=('capacity_Ah', capacity_lim))
    soln_cap = sim.run(expr)
    ts_cap = soln_cap.vars["time_s"]
    phiV_cap = soln_cap.vars["voltage_V"]
    # Capacity limit experiment with no reset
    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600., 10.),
                  limits=('capacity_Ah', capacity_lim/2.0))
    expr.add_step('current_C', 2., (3600., 10.),
                  limits=('capacity_Ah', capacity_lim),
                  reset_capacity=False)
    soln_cap_r = sim.run(expr)
    ts_cap_r = soln_cap_r.vars["time_s"]
    phiV_cap_r = soln_cap_r.vars["voltage_V"]

    # Make sure sim ran for the same time
    end_t_v = ts_v[-1]
    end_t_cap = ts_cap[-1]
    end_t_cap_r = ts_cap_r[-1]
    assert abs(end_t_v - end_t_cap)/end_t_v < 1e-4
    assert abs(end_t_v - end_t_cap_r)/end_t_v < 1e-4

    # Make sure gave the same output
    t_min = max(ts_v.min(), ts_cap.min(), ts_cap_r.min())
    t_max = min(ts_v.max(), ts_cap.max(), ts_cap_r.max())
    t_interp = np.linspace(t_min, t_max, 100)
    phiV_v_int = np.interp(t_interp, ts_v, phiV_v)
    phiV_cap_int = np.interp(t_interp, ts_cap, phiV_cap)
    phiV_cap_r_int = np.interp(t_interp, ts_cap_r, phiV_cap_r)

    assert np.mean(abs(phiV_v_int - phiV_cap_int)) < 1e-4
    assert np.mean(abs(phiV_v_int - phiV_cap_r_int)) < 1e-4

    # Wrong capacity limit experiment
    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600., 10.),
                  limits=('capacity_Ah', capacity_lim/2.0))
    soln_cap = sim.run(expr)
    ts_cap = soln_cap.vars["time_s"]

    # Failed to reset cap
    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600., 10.),
                  limits=('capacity_Ah', capacity_lim/2.0))
    expr.add_step('current_C', 2., (3600., 10.),
                  limits=('capacity_Ah', capacity_lim))
    soln_cap_r = sim.run(expr)
    ts_cap_r = soln_cap_r.vars["time_s"]

    # Make sure sim ran for different time
    end_t_cap = ts_cap[-1]
    end_t_cap_r = ts_cap_r[-1]
    assert abs(end_t_v - end_t_cap)/end_t_v > 1e-4
    assert abs(end_t_v - end_t_cap_r)/end_t_v > 1e-4


def test_phase_clock_limit(sim):
    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600, 0.1), limits=('voltage_V', 3.9))
    expr.add_step('voltage_V', 3.9, (3600, 0.1),
                  limits=('phase_time_s', 100.), reset_timer=True)
    soln = sim.run(expr)
    assert soln.vars["time_s"][-1] > 300

    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600, 0.1), limits=('voltage_V', 3.9))
    expr.add_step('voltage_V', 3.9, (3600, 0.1),
                  limits=('phase_time_s', 100.), reset_timer=False)
    soln = sim.run(expr)
    assert soln.vars["time_s"][-1] < 300

    expr = bm.Experiment()
    expr.add_step('current_C', 2., (3600, 0.1), limits=('voltage_V', 3.9))
    expr.add_step('voltage_V', 3.9, (3600, 0.1),
                  limits=('phase_time_s', 500.), reset_timer=False)
    soln = sim.run(expr)
    assert abs(soln.vars["time_s"][-1] - 500) < 1e-2

