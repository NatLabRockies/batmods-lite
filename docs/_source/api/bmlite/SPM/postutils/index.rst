:py:mod:`bmlite.SPM.postutils`
==============================

.. py:module:: bmlite.SPM.postutils

.. autoapi-nested-parse::

   .. rubric:: Post-processing Utilities

   This module contains all post-processing functions for the SPM package. The
   available post-processing options for a given experiment are specific to that
   experiment. Therefore, not all ``Solution`` classes may have access to all of
   the following functions.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   bmlite.SPM.postutils.current
   bmlite.SPM.postutils.intercalation
   bmlite.SPM.postutils.ivp
   bmlite.SPM.postutils.pixels
   bmlite.SPM.postutils.post
   bmlite.SPM.postutils.potentials
   bmlite.SPM.postutils.power
   bmlite.SPM.postutils.voltage



.. py:function:: current(sol: object, ax: object = None) -> None

   Plot current density vs. time.

   :param sol: A single particle model solution object.
   :type sol: SPM Solution object
   :param ax: An ``axis`` instance from a ``matplotlib`` figure. The default is
              ``None``. If not specified, a new figure is made.
   :type ax: object, optional

   :returns: *None.*


.. py:function:: intercalation(sol: object) -> None

   Plots anode and cathode particle intercalation profiles vs. time.

   :param sol: A single particle model solution object.
   :type sol: SPM Solution object

   :returns: *None.*


.. py:function:: ivp(sol: object) -> None

   Subplots for current, voltage, and power.

   :param sol: A single particle model solution object.
   :type sol: SPM Solution object

   :returns: *None.*


.. py:function:: pixels(sol: object) -> None

   Makes pixel plots for most 2D (space/time) variables.

   :param sol: A pseudo-2D model solution object.
   :type sol: P2D Solution object

   :returns: *None.*


.. py:function:: post(sol: object) -> dict

   Run post processing to determine secondary variables.

   :param sol: A single particle model solution object.
   :type sol: SPM Solution object

   :returns: **postvars** (*dict*) -- Post processed variables, as described below.

             ========= ========================================================
             Key       Value [units] (*type*)
             ========= ========================================================
             res       DAE residual at t (row) for y (col) [units] (*2D array*)
             sdot_an   anode Faradaic current at t [kmol/m^2/s] (*1D array*)
             sdot_ca   cathode Faradaic current at t [kmol/m^2/s] (*1D array*)
             i_ext     external current density at t [A/m^2] (*1D array*)
             A*h/m^2   areal capacity at t [A*h/m^2] (*1D array*)
             ========= ========================================================


.. py:function:: potentials(sol: object) -> None

   Plots anode, electrolyte, and cathode potentials vs. time.

   :param sol: A single particle model solution object.
   :type sol: SPM Solution object

   :returns: *None.*


.. py:function:: power(sol: object, ax: object = None) -> None

   Plot power density vs. time.

   :param sol: A single particle model solution object.
   :type sol: SPM Solution object
   :param ax: An ``axis`` instance from a ``matplotlib`` figure. The default is
              ``None``. If not specified, a new figure is made.
   :type ax: object, optional

   :returns: *None.*


.. py:function:: voltage(sol: object, ax: object = None) -> None

   Plot cell voltage vs. time.

   :param sol: A single particle model solution object.
   :type sol: SPM Solution object
   :param ax: An ``axis`` instance from a ``matplotlib`` figure. The default is
              ``None``. If not specified, a new figure is made.
   :type ax: object, optional

   :returns: *None.*


