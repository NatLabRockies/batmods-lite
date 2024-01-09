:orphan:

:py:mod:`bmlite.P2D.solutions._cv_solution`
===========================================

.. py:module:: bmlite.P2D.solutions._cv_solution


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   bmlite.P2D.solutions._cv_solution.CVSolution




.. py:class:: CVSolution(sim: object, exp: dict)




   Constant voltage solution for P2D simulations.

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

      Class name. Overwrites ``classname()`` from ``BaseSolution``.

      :returns: **classname** (*str*) -- Name of current class.


