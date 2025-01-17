from sksundae import ida


class IDASolver(ida.IDA):
    """
    An IDA solver defined by a residuals function.

    For an ODE or DAE defined as ``M*y' = f(t, y)``, the residuals function is
    ``residuals = M*y' - f(t, y)``. This must be built as a python function
    with a signature like ``def resdiuals(t, y, yp, res, inputs) -> None``.
    The ``res`` parameter must be a 1D array the same size as ``y`` and ``yp``.
    Although the function returns ``None``, the solver uses the filled ``res``
    array to integrate/solve the system. The ``inputs`` parameter is a *tuple*
    that is used to pass any required user-defined ``*args`` to the function.

    Parameters
    ----------
    residuals : Callable
        Residuals function ``def residuals(t, y, yp, res, inputs) -> None``.
        For some examples, see :func:`bmlite.SPM.dae.residuals` and/or
        :func:`bmlite.P2D.dae.residuals`.
    **kwargs : dict, optional
        The keyword arguments specify the Sundials IDA solver options. A
        partial list of options/defaults is given below:

        ============ =========================================================
        Key          Description (*type* or {options}, default)
        ============ =========================================================
        rtol         relative tolerance (*float*, 1e-6)
        atol         absolute tolerance (*float*, 1e-6)
        userdata     the ``inputs`` parameter (*tuple*, ``None``)
        linsolver    linear solver (``{'dense', 'band'}``, ``'dense'``)
        lband        width of the lower band (*int*, 0)
        uband        width of the upper band (*int*, 0)
        rootfn       root/event function (*Callable*, ``None``)
        nr_rootfns   number of events in ``'rootfn'`` (*int*, ``0``)
        initcond     unknown variable set (``{'y0', 'yp0', None}``, ``'yp0'``)
        algidx       algebraic variable indices in y (*list[int]*, ``None``)
        max_step     maximum time step [s] (*float*, 0. -> unrestricted)
        ============ =========================================================

    Notes
    -----
    * The solver name IDA stands for Implicit Differential-Algebraic solver.
      It is part of the `SUNDIALS`_ package, and is accessed here through the
      `scikits-odes`_ python wrapper.
    * The solver can be unstable if the ``algidx`` keyword argument is not
      specified for DAEs.
    * The ``rootfn`` keyword argument must have the signature ``def f(t, y, yp,
      events, inputs) -> None`` where the ``events`` parameter is an array that
      is filled with root functions. If any element in ``events`` hits zero
      during the solver integration, the solver will exit.

      .. _SUNDIALS: https://sundials.readthedocs.io/
      .. _scikits-odes: https://bmcage.github.io/odes/dev/

    """

    def __init__(self, residuals, **kwargs) -> None:

        # Overwrite scikits.odes defaults w/ some keys renamed
        options = {
            'rtol': kwargs.pop('rtol', 1e-6),
            'eventsfn': kwargs.pop('rootfn', None),
            'num_events': kwargs.pop('nr_rootfns', 0),
            'calc_initcond': kwargs.pop('initcond', 'yp0'),
            'algebraic_idx': kwargs.pop('algidx', None),
        }

        # Collect new defaults and any extra user kwargs
        options = {**options, **kwargs}

        super().__init__(residuals, **options)


class IDAResult(ida.IDAResult):
    pass
