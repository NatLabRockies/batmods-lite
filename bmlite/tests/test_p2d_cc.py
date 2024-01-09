from pathlib import Path
import os, pytest, shutil

import numpy as np
import bmlite as bm
import matplotlib.pyplot as plt


@pytest.fixture(scope='session')
def sim():
    sim = bm.P2D.Simulation()
    return sim


@pytest.fixture(scope='session')
def CCsim():
    CCsim = bm.P2D.Simulation()
    CCsim.run_CC(rtol=1e-6, atol=1e-9)
    return CCsim


def test_fake_yaml():
    with pytest.raises(Exception):
        bm.P2D.Simulation('fake_yaml')

    assert True


def test_run_CC(CCsim):
    assert CCsim.sol.values.t[-1] == CCsim.bat.t_max


def test_post_vars(sim, CCsim):
    with pytest.raises(Exception):
        sim.post()

    CCsim.post()
    assert hasattr(CCsim, 'post_vars')


def test_post_debug(CCsim):
    CCsim.post(debug=1)
    plt.close('all')
    assert True


def test_post_verify(CCsim):
    CCsim.post(verify=1)
    plt.close('all')

    i_ext = CCsim.bat.i_ext
    err_tol = 0.5/100*CCsim.bat.i_ext

    el, an, sep, ca = CCsim.el, CCsim.an, CCsim.sep, CCsim.ca

    an_int = CCsim.post_vars['sdot_an']*an.A_s*bm.c.F*(an.xp - an.xm)
    an_chk = np.sum(an_int, axis=1)
    assert np.max(np.abs(an_chk + i_ext)) <= np.abs(err_tol)

    ca_int = CCsim.post_vars['sdot_ca']*ca.A_s*bm.c.F*(ca.xp - ca.xm)
    ca_chk = np.sum(ca_int, axis=1)
    assert np.max(np.abs(ca_chk - i_ext)) <= np.abs(err_tol)

    Li_el_an = CCsim.sol.values.y[:, an.x_ptr('Li_el')]
    Li_el_sep = CCsim.sol.values.y[:, sep.x_ptr('Li_el')]
    Li_el_ca = CCsim.sol.values.y[:, ca.x_ptr('Li_el')]

    eps_Li_x = np.hstack([Li_el_an*an.eps_el*(an.xp - an.xm),
                          Li_el_sep*sep.eps_el*(sep.xp - sep.xm),
                          Li_el_ca*ca.eps_el*(ca.xp - ca.xm)])

    eps_Li_0 = np.hstack([el.Li_0*an.eps_el*(an.xp - an.xm),
                          el.Li_0*sep.eps_el*(sep.xp - sep.xm),
                          el.Li_0*ca.eps_el*(ca.xp - ca.xm)])

    err_tol = 0.5/100*np.sum(eps_Li_0)

    el_chk = np.sum(eps_Li_x, axis=1) - np.sum(eps_Li_0)
    assert np.max(np.abs(el_chk)) <= err_tol

    assert np.allclose(CCsim.post_vars['i_el_x'][:, 0], 0.)
    assert np.allclose(CCsim.post_vars['i_el_x'][:, -1], 0.)

    i_ext = CCsim.bat.i_ext
    err_tol = 0.5/100*CCsim.bat.i_ext

    assert np.all(np.abs(CCsim.post_vars['sum_ip'] + i_ext) <= np.abs(err_tol))


def test_post_gen_plots(CCsim):
    CCsim.post(gen_plots=1)
    plt.close('all')
    assert True


def test_post_waterfall(CCsim):
    CCsim.post(waterfall=1)
    plt.close('all')
    assert True


def test_save(sim, CCsim):
    with pytest.raises(Exception):
        sim.save('p2d_save')

    CCsim.save('p2d_save')
    assert True


def test_save_overwrite(CCsim):
    with pytest.raises(Exception):
        CCsim.save('p2d_save')

    CCsim.save('p2d_save', overwrite=1)
    assert True


def test_load(CCsim):
    loaded_sim = bm.P2D.load('p2d_save')
    path = Path(os.path.dirname(__file__) + '/../../Results')
    shutil.rmtree(path)
    assert np.allclose(loaded_sim.sol.values.y, CCsim.sol.values.y)


def test_slice_and_save(sim, CCsim):
    with pytest.raises(Exception):
        sim.slice_and_save('p2d_save')

    CCsim.slice_and_save('p2d_save')
    loaded_sol = np.load('p2d_save.npz')
    loaded_ce_a = loaded_sol['ce_a']
    current_ce_a = CCsim.sol.values.y[:, CCsim.an.x_ptr('Li_el')]
    loaded_sol.close()

    path = Path(os.path.dirname(__file__) + '/../../p2d_save.npz')
    os.remove(path)
    assert np.allclose(loaded_ce_a, current_ce_a)
