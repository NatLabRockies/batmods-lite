bmlite.P2D.postutils
====================

.. py:module:: bmlite.P2D.postutils

.. autoapi-nested-parse::

   .. rubric:: Post-processing Utilities

   This module contains all post-processing functions for the P2D package. The
   available post-processing options for a given experiment are specific to that
   experiment. Therefore, not all ``Solution`` classes may have access to all of
   the following functions.



Functions
---------

.. autoapisummary::

   bmlite.P2D.postutils.current
   bmlite.P2D.postutils.electrolyte
   bmlite.P2D.postutils.intercalation
   bmlite.P2D.postutils.ivp
   bmlite.P2D.postutils.pixels
   bmlite.P2D.postutils.post
   bmlite.P2D.postutils.potentials
   bmlite.P2D.postutils.power
   bmlite.P2D.postutils.voltage


Module Contents
---------------

.. py:function:: current(sol, ax = None)

   Plot current density vs. time.

   :param sol: A pseudo-2D model solution object.
   :type sol: P2D Solution object
   :param ax: An ``axis`` instance from a ``matplotlib`` figure. The default is
              ``None``. If not specified, a new figure is made.
   :type ax: object, optional

   :returns: *None.*


.. py:function:: electrolyte(sol)

   Plots electrolyte Li-ion concentration profiles vs. time.

   :param sol: A pseudo-2D model solution object.
   :type sol: P2D Solution object

   :returns: *None.*


.. py:function:: intercalation(sol)

   Plots anode and cathode particle intercalation profiles vs. time.

   :param sol: A pseudo-2D model solution object.
   :type sol: P2D Solution object

   :returns: *None.*


.. py:function:: ivp(sol)

   Subplots for current, voltage, and power.

   :param sol: A pseudo-2D model solution object.
   :type sol: P2D Solution object

   :returns: *None.*


.. py:function:: pixels(sol)

   Makes pixel plots for most 2D (space/time) variables.

   :param sol: A pseudo-2D model solution object.
   :type sol: P2D Solution object

   :returns: *None.*


.. py:function:: post(sol)

   Run post processing to determine secondary variables.

   :param sol: A pseudo-2D model solution object.
   :type sol: P2D Solution object

   :returns: **postvars** (*dict*) -- Post processed variables, as described below.

             =========== ========================================================
             Key         Value [units] (*type*)
             =========== ========================================================
             res         DAE residual at t (row) for y (col) [units] (*2D array*)
             div_i_an    divergence of current at t, x_a [A/m^3] (*2D array*)
             div_i_sep   divergence of current at t, x_s [A/m^3] (*2D array*)
             div_i_ca    divergence of current at t, x_c [A/m^3] (*2D array*)
             sdot_an     Faradaic current at t, x_a [kmol/m^2/s] (*1D array*)
             sdot_ca     Faradaic current at t, x_c [kmol/m^2/s] (*1D array*)
             sum_ip      ``i_ed + i_el`` at t, xp interfaces [A/m^2] (*2D array*)
             i_el_x      ``i_el`` at t, x interfaces [A/m^2] (*2D array*)
             i_ext       external current density at t [A/m^2] (*1D array*)
             A*h/m^2     areal capacity at t [A*h/m^2] (*1D array*)
             =========== ========================================================


.. py:function:: potentials(sol)

   Plots anode, electrolyte, and cathode potentials vs. time and space.

   :param sol: A pseudo-2D model solution object.
   :type sol: P2D Solution object

   :returns: *None.*


.. py:function:: power(sol, ax = None)

   Plot power density vs. time.

   :param sol: A pseudo-2D model solution object.
   :type sol: P2D Solution object
   :param ax: An ``axis`` instance from a ``matplotlib`` figure. The default is
              ``None``. If not specified, a new figure is made.
   :type ax: object, optional

   :returns: *None.*


.. py:function:: voltage(sol, ax = None)

   Plot cell voltage vs. time.

   :param sol: A pseudo-2D model solution object.
   :type sol: P2D Solution object
   :param ax: An ``axis`` instance from a ``matplotlib`` figure. The default is
              ``None``. If not specified, a new figure is made.
   :type ax: object, optional

   :returns: *None.*


