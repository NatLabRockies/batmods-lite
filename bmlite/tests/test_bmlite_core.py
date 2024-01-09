import bmlite as bm


def test_faradays_constant():
    assert bm.c.F == 96485.3321e3


def test_gas_constant():
    assert bm.c.R == 8.3145e3


def test_spm_construction():
    sim = bm.SPM.Simulation()
    assert hasattr(sim, 'bat')
    assert hasattr(sim, 'el')
    assert hasattr(sim, 'an')
    assert hasattr(sim, 'ca')


def test_p2d_construction():
    sim = bm.P2D.Simulation()
    assert hasattr(sim, 'bat')
    assert hasattr(sim, 'el')
    assert hasattr(sim, 'an')
    assert hasattr(sim, 'sep')
    assert hasattr(sim, 'ca')
