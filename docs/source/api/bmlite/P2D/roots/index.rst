bmlite.P2D.roots
================

.. py:module:: bmlite.P2D.roots

.. autoapi-nested-parse::

   .. rubric:: Root Functions

   This module includes root functions for the SPM model. Root functions allow the
   integrator to stop prior to ``t_max`` when an event (or root) occurs. For
   example, during a typical CCCV charge protocol, it is common to stop and switch
   from constant-current to constant-voltage at a specified voltage.



Classes
-------

.. autoapisummary::

   bmlite.P2D.roots.ILimits
   bmlite.P2D.roots.VLimits


Module Contents
---------------

.. py:class:: ILimits(I_low, I_high)



   
   Generate a root function that stops at current limits.

   :param I_low: The desired low current limit [A], + for charge, - for discharge.
   :type I_low: float
   :param I_high: The desired high current limit [A], + for charge, - for discharge.
   :type I_high: float

   .. rubric:: Notes

   To use a root function, you will have to create an instance, and then
   pass both the root function, and the number of root functions to the
   solver. The number of roots is stored as the property ``size``.

   .. rubric:: Example

   >>> sim = bm.P2D.Simulation()
   >>> exp = {'V_ext': 3.8, 't_min': 0., 't_max': 1350., 'Nt': 1351}
   >>> rootfn = bm.P2D.roots.ILimits(-0.45 * sim.bat.area, np.nan)
   >>> sol = sim.run_CV(exp, rootfn=rootfn, nr_rootfns=rootfn.size)
   >>> sol.plot('ivp')


   .. py:property:: size
      Number of roots in the root function instance.

      :returns: **size** (*int*) -- The size of the events array in the root function.


.. py:class:: VLimits(V_low, V_high)



   
   Generate a root function that stops at voltage limits.

   :param V_low: The desired low voltage limit [V].
   :type V_low: float
   :param V_high: The desired high voltage limit [V].
   :type V_high: float

   .. rubric:: Notes

   To use a root function, you will have to create an instance, and then
   pass both the root function, and the number of root functions to the
   solver. The number of roots is stored as the property ``size``.

   .. rubric:: Example

   >>> sim = bm.P2D.Simulation()
   >>> exp = {'C_rate': -2., 't_min': 0., 't_max': 3600., 'Nt': 3601}
   >>> rootfn = bm.P2D.roots.VLimits(3.0, np.nan)
   >>> sol = sim.run_CC(exp, rootfn=rootfn, nr_rootfns=rootfn.size)
   >>> sol.plot('ivp')


   .. py:property:: size
      Number of roots in the root function instance.

      :returns: **size** (*int*) -- The size of the events array in the root function.


