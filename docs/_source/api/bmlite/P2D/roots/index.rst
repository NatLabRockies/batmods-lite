:py:mod:`bmlite.P2D.roots`
==========================

.. py:module:: bmlite.P2D.roots

.. autoapi-nested-parse::

   .. rubric:: Root Functions

   This module includes root functions for the SPM model. Root functions allow the
   integrator to stop prior to ``t_max`` when an event (or root) occurs. For
   example, during a typical CCCV charge protocol, it is common to stop and switch
   from constant-current to constant-voltage at a specified voltage.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   bmlite.P2D.roots.ILimits
   bmlite.P2D.roots.VLimits




.. py:class:: ILimits(I_low: float, I_high: float)




   
   Generate a root function that stops at current limits.

   :param I_low: The desired low current limit [A], + for charge, - for discharge.
   :type I_low: float
   :param I_high: The desired high current limit [A], + for charge, - for discharge.
   :type I_high: float


.. py:class:: VLimits(V_low: float, V_high: float)




   
   Generate a root function that stops at voltage limits.

   :param V_low: The desired low voltage limit [V].
   :type V_low: float
   :param V_high: The desired high voltage limit [V].
   :type V_high: float


