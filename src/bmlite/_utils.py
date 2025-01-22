import atexit
import warnings
from typing import Callable


class ExitHandler:
    """
    Exit handler.

    Use this class to register functions that you want to run just before a
    file exits. This is primarily used to register plt.show() so plots appear
    in both interactive and non-interactive environments, even if the user
    forgets to explicitly call it.

    """
    _registered = []

    @classmethod
    def register_atexit(cls, func: Callable) -> None:
        if func not in cls._registered:
            atexit.register(func)


def formatwarning(message, category, filename, lineno, line=None):
    """Shortened warning format - used for parameter/pre warnings."""
    return f"\n[bmlite {category.__name__}] {message}\n\n"


def short_warn(message, category=None, stacklevel=1, source=None):
    """Print a warning with the short format from ``formatwarning``."""
    original_format = warnings.formatwarning

    warnings.formatwarning = formatwarning
    warnings.warn(message, category, stacklevel, source)

    warnings.formatwarning = original_format
