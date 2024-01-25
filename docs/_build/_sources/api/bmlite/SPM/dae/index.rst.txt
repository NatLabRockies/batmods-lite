:py:mod:`bmlite.SPM.dae`
========================

.. py:module:: bmlite.SPM.dae

.. autoapi-nested-parse::

   .. rubric:: DAE Module

   This module includes the system of differential algebraic equations (DAE) for
   the SPM model. In addition, the ``bandwidth`` function is included in this
   module, which helps determine the lower and upper bandwidths of ``residuals``
   so the ``'band'`` linear solver option can be used in the ``IDASolver`` class.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   bmlite.SPM.dae.bandwidth
   bmlite.SPM.dae.residuals



.. py:function:: bandwidth(sim: object) -> tuple[int | numpy.ndarray]

   Determine the DAE system's bandwidth and Jacobian pattern.

   Numerically determines the bandwidth and Jacobian pattern of the residual
   function by perturbating each ``y`` and ``yp`` term and determining which
   ``dres/dy`` and ``dres/dy'`` terms are non-zero. The bandwidth is required
   to use the "band" option for IDA's linear solver, which speeds up each
   integration step compared to the "dense" linear solver.

   :param inputs: An instance of the SPM model simulation. See
                  :class:`bmlite.SPM.Simulation`.
   :type inputs: SPM Simulation object

   :returns: * **lband** (*int*) -- Lower bandwidth from the residual function's Jacobian pattern.
             * **uband** (*int*) -- Upper bandwidth from the residual function's Jacobian pattern.
             * **j_pat** (*2D array*) -- Residual function Jacobian pattern, as an array of ones and zeros.


.. py:function:: residuals(t: float, sv: numpy.ndarray, svdot: numpy.ndarray, res: numpy.ndarray, inputs: tuple[object, dict]) -> None | tuple[numpy.ndarray]

   The DAE residuals ``res = M*y' - f(t, y)`` for the SPM model.

   :param t: Value of time [s].
   :type t: float
   :param sv: Solution/state variables at time ``t``.
   :type sv: 1D array
   :param svdot: Solution/state variable time derivatives at time ``t``.
   :type svdot: 1D array
   :param res: An array the same size as ``sv`` and ``svdot``. The values are filled
               in with ``res = M*y' - f(t, y)`` inside this function.
   :type res: 1D array
   :param inputs: The simulation object and experimental details dictionary inputs that
                  describe the specific battery and experiment to simulate.
   :type inputs: (sim : SPM Simulation object, exp : experiment dict)

   :returns: * *None* -- If no ``sim._flags`` are ``True``.
             * **res** (*1D array*) -- Array of residuals if ``sim._flags['band'] = True``.
             * **outputs** (*tuple[1D array]*) -- If ``sim._flags['post'] = True`` then ``outputs`` is returned, which
               includes post-processed values. These can help verify the governing
               equations and boundary conditions are satisfied. They can also be
               useful for interpreting causes of good/bad battery performance. The
               order and description of the arrays is given below:

               ========== =======================================================
               Variable   Description [units] (*type*)
               ========== =======================================================
               res        residuals ``res = M*y' - f(t, y)`` [units] (*1D array*)
               sdot_an    anode Li+ production rate [kmol/m^3/s] (*float*)
               sdot_ca    cathode Li+ production rate [kmol/m^3/s] (*float*)
               ========== =======================================================


