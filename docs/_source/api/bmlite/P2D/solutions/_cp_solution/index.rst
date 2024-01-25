:orphan:

:py:mod:`bmlite.P2D.solutions._cp_solution`
===========================================

.. py:module:: bmlite.P2D.solutions._cp_solution


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   bmlite.P2D.solutions._cp_solution.CPSolution




.. py:class:: CPSolution(sim: object, exp: dict)




   Constant power solution for P2D simuations.

   Base: :class:`~bmlite.P2D.solutions.BaseSolution`

   When initialized, a copy of the P2D simulation object and experimental
   details for the solution instance are stored, all other instance
   attributes are set to ``None``. These are filled later with a "fill"
   method (e.g., ``ida_fill()`` or ``dict_fill()``).

   :param sim: The P2D Simulation instance used to produce the solution.
   :type sim: P2D Simulation object
   :param exp: Experiment dictionary. Specific key/value pairs are dependent on
               the experiment that was run.
   :type exp: dict

   .. py:property:: classname
      :type: str

      Class name. Overwrites ``BaseSolution``.

      :returns: **classname** (*str*) -- Name of current class.

   .. py:method:: verify(plotflag: bool = False, rtol: float = 0.005, atol: float = 0.001) -> bool

      Verifies the solution is consistent.

      Specifically, for a constant power experiment, this method checks
      that the calculated power was within tolerance of the boundary
      condition. In addition, this method checks the anodic and cathodic
      Faradaic currents against the current at each time step, the
      through-current in each control volume, and the Li-ion and solid-phase
      lithium conservation.

      You can see which checks failed using the ``plotflag``. Any subplots
      shaded grey failed their test. Note that the third row of the figure
      shows conservation of charge in each control volume in each domain.
      This row is not included in the checks and will never shade grey, but
      is useful in debugging. Notably, high divergence terms generally
      suggest that the solver's relative and/or absolute tolerance should
      be adjusted.

      :param plotflag: A flag to see plots showing the verification calculations. The
                       default is ``False``.
      :type plotflag: bool, optional
      :param rtol: The relative tolerance for array comparisons. The default is 5e-3.
      :type rtol: float, optional
      :param atol: The relative tolerance for array comparisons. The default is 1e-3.
      :type atol: float, optional

      :returns: **checks** (*bool*) -- ``True`` is all checks are satisfied, ``False`` otherwise.



