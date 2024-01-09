import pytest

import numpy as np
import bmlite as bm


@pytest.fixture(scope='session')
def args():
    alpha_a = 0.5
    alpha_c = 0.5
    Li_max = 50.
    return alpha_a, alpha_c, Li_max


def test_gen2_electrolyte():
    el = bm.materials.Gen2Electrolyte()

    C_Li = np.array([1.2, 1.4])

    assert np.allclose(el.get_D(1.0, 303.15), 1.58571930e-10, atol=1e-14)
    assert np.allclose(el.get_D(C_Li, 303.15), [1.35029958e-10, 1.145972e-10],
                       atol=1e-14)

    assert np.allclose(el.get_t0(1.0, 303.15), 0.45967069)
    assert np.allclose(el.get_t0(C_Li, 303.15), [0.46292429, 0.46599655])

    assert np.allclose(el.get_kappa(1.0, 303.15), 0.97656228)
    assert np.allclose(el.get_kappa(C_Li, 303.15), [0.97273979, 0.93240961])

    assert np.allclose(el.get_gamma(1.0, 303.15), 2.20537457)
    assert np.allclose(el.get_gamma(C_Li, 303.15), [2.86877462, 3.66005716])


def test_graphite_fast(args):
    gr = bm.materials.GraphiteFast(args[0], args[1], args[2])

    assert gr.alpha_a == args[0]
    assert gr.alpha_c == args[1]
    assert gr.Li_max == args[2]

    x = np.array([0.75, 0.98])

    assert np.allclose(gr.get_Ds(0.25, 303.15), 3.0e-14, atol=1e-18)
    assert np.allclose(gr.get_Ds(x, 303.15), [3.0e-14, 3.0e-14], atol=1e-18)

    assert np.allclose(gr.get_i0(0.25, 1.2, 303.15), 16.00903065)
    assert np.allclose(gr.get_i0(x, 1.2, 303.15), [16.00903065,  5.17597817])

    assert np.allclose(gr.get_Eeq(0.25, 303.15), 0.12185042)
    assert np.allclose(gr.get_Eeq(x, 303.15), [0.07350187, 0.01585165])


def test_graphite_slow(args):
    gr = bm.materials.GraphiteSlow(args[0], args[1], args[2])

    assert gr.alpha_a == args[0]
    assert gr.alpha_c == args[1]
    assert gr.Li_max == args[2]

    x = np.array([0.75, 0.98])

    assert np.allclose(gr.get_Ds(0.25, 303.15), 3.0e-14, atol=1e-18)
    assert np.allclose(gr.get_Ds(x, 303.15), [3.0e-14, 3.0e-14], atol=1e-18)

    assert np.allclose(gr.get_i0(0.25, 1.2, 303.15), 16.00903065)
    assert np.allclose(gr.get_i0(x, 1.2, 303.15), [16.00903065,  5.17597817])

    assert np.allclose(gr.get_Eeq(0.25, 303.15), 0.14283605)
    assert np.allclose(gr.get_Eeq(x, 303.15), [0.10035986, 0.02679])


def test_nmc_532_fast(args):
    nmc = bm.materials.NMC532Fast(args[0], args[1], args[2])

    assert nmc.alpha_a == args[0]
    assert nmc.alpha_c == args[1]
    assert nmc.Li_max == args[2]

    x = np.array([0.75, 0.98])

    assert np.allclose(nmc.get_Ds(0.25, 303.15), 2.25630659e-16, atol=1e-20)
    assert np.allclose(nmc.get_Ds(x, 303.15), [2.36737202e-15, 1.92455666e-15],
                       atol=1e-20)

    assert np.allclose(nmc.get_i0(0.25, 1.2, 303.15), 2.82890928)
    assert np.allclose(nmc.get_i0(x, 1.2, 303.15), [2.39367959, 0.96017122])

    assert np.allclose(nmc.get_Eeq(0.25, 303.15), 4.51083696)
    assert np.allclose(nmc.get_Eeq(x, 303.15), [3.73531924, 3.53325221])


def test_nmc_532_slow(args):
    nmc = bm.materials.NMC532Slow(args[0], args[1], args[2])

    assert nmc.alpha_a == args[0]
    assert nmc.alpha_c == args[1]
    assert nmc.Li_max == args[2]

    x = np.array([0.75, 0.98])

    assert np.allclose(nmc.get_Ds(0.25, 303.15), 2.25630659e-16, atol=1e-20)
    assert np.allclose(nmc.get_Ds(x, 303.15), [2.36737202e-15, 1.92455666e-15],
                       atol=1e-20)

    assert np.allclose(nmc.get_i0(0.25, 1.2, 303.15), 2.82890928)
    assert np.allclose(nmc.get_i0(x, 1.2, 303.15), [2.39367959, 0.96017122])

    assert np.allclose(nmc.get_Eeq(0.25, 303.15), 0.)
    assert np.allclose(nmc.get_Eeq(x, 303.15), [3.74209879, 3.56861776])
