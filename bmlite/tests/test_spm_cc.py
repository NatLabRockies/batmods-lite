from pathlib import Path
import os, pytest, shutil

import numpy as np
import bmlite as bm
import matplotlib.pyplot as plt


@pytest.fixture(scope='session')
def sim():
    sim = bm.SPM.Simulation()
    return sim


@pytest.fixture(scope='session')
def CCsim():
    CCsim = bm.SPM.Simulation()
    CCsim.run_CC(rtol=1e-6, atol=1e-9)
    return CCsim


def test_fake_yaml():
    with pytest.raises(Exception):
        bm.SPM.Simulation('fake_yaml')

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

    an_chk = CCsim.post_vars['sdot_an']*CCsim.an.A_s*bm.c.F*CCsim.an.thick
    assert np.max(np.abs(an_chk + i_ext)) <= np.abs(err_tol)

    ca_chk = CCsim.post_vars['sdot_ca']*CCsim.ca.A_s*bm.c.F*CCsim.ca.thick
    assert np.max(np.abs(ca_chk - i_ext)) <= np.abs(err_tol)


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
        sim.save('spm_save')

    CCsim.save('spm_save')
    assert True


def test_save_overwrite(CCsim):
    with pytest.raises(Exception):
        CCsim.save('spm_save')

    CCsim.save('spm_save', overwrite=1)
    assert True


def test_load(CCsim):
    loaded_sim = bm.SPM.load('spm_save')
    path = Path(os.path.dirname(__file__) + '/../../Results')
    shutil.rmtree(path)
    assert np.allclose(loaded_sim.sol.values.y, CCsim.sol.values.y)


def test_slice_and_save(sim, CCsim):
    with pytest.raises(Exception):
        sim.slice_and_save('spm_save')

    CCsim.slice_and_save('spm_save')
    loaded_sol = np.load('spm_save.npz')
    loaded_cs_a = loaded_sol['cs_a']
    current_cs_a = CCsim.sol.values.y[:, CCsim.an.r_ptr('Li_ed')]
    loaded_sol.close()

    path = Path(os.path.dirname(__file__) + '/../../spm_save.npz')
    os.remove(path)
    assert np.allclose(loaded_cs_a, current_cs_a)
