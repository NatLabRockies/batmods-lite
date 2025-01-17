class Constants:
    """Physical constants."""

    __slots__ = ()

    _F = 96485.3321e3
    _R = 8.3145e3

    @property
    def F(self) -> float:
        """Faraday's constant [C/kmol]."""
        return self._F

    @property
    def R(self) -> float:
        """Gas constant [J/kmol/K]."""
        return self._R
