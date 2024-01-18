import pytest

import bmlite as bm


@pytest.fixture(scope='session')
def c():
    c = bm.Constants()
    return c


def test_constants_read_only(c):
    with pytest.raises(AttributeError):
        c.F = 1

    with pytest.raises(AttributeError):
        c.R = 1

    with pytest.raises(AttributeError):
        c.a = 1


def test_constants_empty_slots(c):
    assert c.__slots__ == []


def test_constants_faradays(c):
    assert c.F == 96485.3321e3


def test_constants_ideal_gas(c):
    assert c.R == 8.3145e3


def test_docs():
    bm.docs()

    assert True


def test_format_ticks():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5, 3.5])
    bm.format_ax(ax)

    assert True
