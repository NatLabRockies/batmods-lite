import pytest

from bmlite._utils import ProgressBar


def test_progbar_initialization():

    with pytest.raises(ValueError, match='conflicting'):
        _ = ProgressBar(iterable=[1, 2, 3], manual=True)

    with pytest.raises(ValueError, match='cannot be None'):
        _ = ProgressBar(iterable=None, manual=False)

    bar = ProgressBar(iterable=[1, 2, 3])
    assert bar._manual is False
    assert bar.total == 3

    bar = ProgressBar(manual=True)
    assert bar._manual is True
    assert bar.total == 1


def test_iterable_progbar():
    iterable = range(10)

    bar = ProgressBar(iterable)
    for i in bar:
        pass

    assert bar._manual is False


def test_manual_progbar():

    bar = ProgressBar(manual=True)
    for i in range(10):
        bar.set_progress(0.1*(i+1))

    assert bar._manual is True
    assert bar._iter == 10

    bar.reset()
    assert bar._iter == 0
