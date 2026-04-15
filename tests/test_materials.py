import os

import pytest
import numpy as np
import bmlite as bm
import pandas as pd


@pytest.fixture(scope='module')
def args():
    alpha_a = 0.5
    alpha_c = 0.5
    Li_max = 50.
    return alpha_a, alpha_c, Li_max


def test_gen2_electrolyte():
    el = bm.materials.Gen2Electrolyte()

    directory = os.path.dirname(__file__)
    data = np.load(directory + '/materials_data/gen2electrolyte.npz')

    C_Li, T = data['C_Li'], data['T']

    D = el.get_D(C_Li, T)
    assert np.allclose(D / max(D), data['D'] / max(D))

    t0 = el.get_t0(C_Li, T)
    assert np.allclose(t0 / max(t0), data['t0'] / max(t0))

    kappa = el.get_kappa(C_Li, T)
    assert np.allclose(kappa / max(kappa), data['kappa'] / max(kappa))

    gamma = el.get_gamma(C_Li, T)
    assert np.allclose(gamma / max(gamma), data['gamma'] / max(gamma))

    data.close()


def test_graphite_fast(args):
    gr = bm.materials.GraphiteFast(args[0], args[1], args[2])

    directory = os.path.dirname(__file__)
    data = np.load(directory + '/materials_data/graphitefast.npz')

    x, C_Li, T = data['x'], data['C_Li'], data['T']

    Ds = gr.get_Ds(x, T, fluxdir=0)
    assert np.allclose(Ds / max(Ds), data['Ds'] / max(Ds))

    i0 = gr.get_i0(x, C_Li, T, fluxdir=0)
    assert np.allclose(i0 / max(i0), data['i0'] / max(i0))

    Eeq = gr.get_Eeq(x)
    assert np.allclose(Eeq / max(Eeq), data['Eeq'] / max(Eeq))

    data.close()


def test_graphite_slow(args):
    gr = bm.materials.GraphiteSlow(args[0], args[1], args[2])

    directory = os.path.dirname(__file__)
    data = np.load(directory + '/materials_data/graphiteslow.npz')

    x, C_Li, T = data['x'], data['C_Li'], data['T']

    Ds = gr.get_Ds(x, T, fluxdir=0)
    assert np.allclose(Ds / max(Ds), data['Ds'] / max(Ds))

    i0 = gr.get_i0(x, C_Li, T, fluxdir=0)
    assert np.allclose(i0 / max(i0), data['i0'] / max(i0))

    Eeq = gr.get_Eeq(x)
    assert np.allclose(Eeq / max(Eeq), data['Eeq'] / max(Eeq))

    data.close()

    with pytest.raises(ValueError):
        gr.get_Eeq(gr.x_min - 0.01)

    with pytest.raises(ValueError):
        gr.get_Eeq(gr.x_max * np.ones(5) + 0.01)


def test_nmc_532_fast(args):
    nmc = bm.materials.NMC532Fast(args[0], args[1], args[2])

    directory = os.path.dirname(__file__)
    data = np.load(directory + '/materials_data/nmc532fast.npz')

    x, C_Li, T = data['x'], data['C_Li'], data['T']

    Ds = nmc.get_Ds(x, T, fluxdir=0)
    assert np.allclose(Ds / max(Ds), data['Ds'] / max(Ds))

    i0 = nmc.get_i0(x, C_Li, T, fluxdir=0)
    assert np.allclose(i0 / max(i0), data['i0'] / max(i0))

    Eeq = nmc.get_Eeq(x)
    assert np.allclose(Eeq / max(Eeq), data['Eeq'] / max(Eeq))

    data.close()


def test_nmc_532_slow(args):
    nmc = bm.materials.NMC532Slow(args[0], args[1], args[2])

    directory = os.path.dirname(__file__)
    data = np.load(directory + '/materials_data/nmc532slow.npz')

    x, C_Li, T = data['x'], data['C_Li'], data['T']

    Ds = nmc.get_Ds(x, T, fluxdir=0)
    assert np.allclose(Ds / max(Ds), data['Ds'] / max(Ds))

    i0 = nmc.get_i0(x, C_Li, T, fluxdir=0)
    assert np.allclose(i0 / max(i0), data['i0'] / max(i0))

    Eeq = nmc.get_Eeq(x)
    assert np.allclose(Eeq / max(Eeq), data['Eeq'] / max(Eeq))

    data.close()

    with pytest.raises(ValueError):
        nmc.get_Eeq(nmc.x_min - 0.01)

    with pytest.raises(ValueError):
        nmc.get_Eeq(nmc.x_max * np.ones(5) + 0.01)


def test_nmc_811(args):
    nmc = bm.materials.NMC811(args[0], args[1], args[2])

    directory = os.path.dirname(__file__)
    data = np.load(directory + '/materials_data/nmc811.npz')

    x, C_Li, T = data['x'], data['C_Li'], data['T']

    Ds = nmc.get_Ds(x, T, fluxdir=0)
    assert np.allclose(Ds / max(Ds), data['Ds'] / max(Ds))

    i0 = nmc.get_i0(x, C_Li, T, fluxdir=0)
    assert np.allclose(i0 / max(i0), data['i0'] / max(i0))

    Eeq = nmc.get_Eeq(x)
    assert np.allclose(Eeq / max(Eeq), data['Eeq'] / max(Eeq))

    data.close()


def test_nmc_811_slow(args, tmp_path):

    # Make sure we get a FileNotFoundError if we don't
    # pass a csvfile
    try:
        nmc = bm.materials.NMC811Slow(args[0], args[1], args[2])
    except FileNotFoundError:
        pass

    directory = os.path.dirname(__file__)
    data = np.load(directory + '/materials_data/nmc811.npz')
    x, C_Li, T = data['x'], data['C_Li'], data['T']

    data_ocv = {
        'x': [0.0, 0.25, 0.5, 0.75, 1.0],
        'V': [4.2, 4.0,  3.7, 3.5,  2.5]
    }

    # Write fake csv file that contains the fake OCV
    save_path = os.path.join(tmp_path, "dummy_ocv.csv")
    df = pd.DataFrame(data_ocv)
    df.to_csv(save_path)

    nmc = bm.materials.NMC811Slow(args[0], args[1], args[2],
                                  csvfile=save_path)

    # Should be unchanged compared to the non slow version
    Ds = nmc.get_Ds(x, T, fluxdir=0)
    assert np.allclose(Ds / max(Ds), data['Ds'] / max(Ds))

    # Should be unchanged compared to the non slow version
    i0 = nmc.get_i0(x, C_Li, T, fluxdir=0)
    assert np.allclose(i0 / max(i0), data['i0'] / max(i0))

    Eeq = nmc.get_Eeq(x)
    is_within = (Eeq >= 2).all() and (Eeq <= 5).all()
    assert is_within

    data.close()


def test_graphite_siox(args):
    grsiox = bm.materials.GraphiteSiOx(args[0], args[1], args[2])

    directory = os.path.dirname(__file__)
    data = np.load(directory + '/materials_data/graphite_SiOx.npz')

    x, C_Li, T = data['x'], data['C_Li'], data['T']

    Ds = grsiox.get_Ds(x, T, fluxdir=0)
    assert np.allclose(Ds / max(Ds), data['Ds'] / max(Ds))

    i0 = grsiox.get_i0(x, C_Li, T, fluxdir=0)
    assert np.allclose(i0 / max(i0), data['i0'] / max(i0))

    Eeq = grsiox.get_Eeq(x)
    assert np.allclose(Eeq / max(Eeq), data['Eeq'] / max(Eeq))

    data.close()


def test_graphite_siox_slow(args, tmp_path):

    # Make sure we get a FileNotFoundError if we don't
    # pass a csvfile
    try:
        grsiox = bm.materials.GraphiteSiOxSlow(args[0], args[1], args[2])
    except FileNotFoundError:
        pass

    directory = os.path.dirname(__file__)
    data = np.load(directory + '/materials_data/graphite_SiOx.npz')
    x, C_Li, T = data['x'], data['C_Li'], data['T']

    data_ocv = {
        'x': [0.0, 0.25, 0.5, 0.75, 1.0],
        'V': [1.2, 1.0,  0.7, 0.5,  0.0]
    }

    # Write fake csv file that contains the fake OCV
    save_path = os.path.join(tmp_path, "dummy_ocv.csv")
    df = pd.DataFrame(data_ocv)
    df.to_csv(save_path)

    grsiox = bm.materials.GraphiteSiOxSlow(args[0], args[1], args[2],
                                           csvfile=save_path)

    # Should be unchanged compared to the non slow version
    Ds = grsiox.get_Ds(x, T, fluxdir=0)
    assert np.allclose(Ds / max(Ds), data['Ds'] / max(Ds))

    # Should be unchanged compared to the non slow version
    i0 = grsiox.get_i0(x, C_Li, T, fluxdir=0)
    assert np.allclose(i0 / max(i0), data['i0'] / max(i0))

    Eeq = grsiox.get_Eeq(x)
    is_within = (Eeq >= -0.1).all() and (Eeq <= 1.5).all()
    assert is_within

    data.close()
