:orphan:

:py:mod:`bmlite.materials._gen2_electrolyte`
============================================

.. py:module:: bmlite.materials._gen2_electrolyte


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   bmlite.materials._gen2_electrolyte.Gen2Electrolyte




.. py:class:: Gen2Electrolyte




   
   Gen 2 Electrolyte transport and material properties.

   .. py:method:: get_D(C_Li, T)

      Calculate the lithium ion diffusivity in the electrolyte solution at
      concentration ``C_Li`` and temperature ``T``.

      :param C_Li: Lithium ion concentration in the electrolyte [kmol/m^3].
      :type C_Li: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **D** (*float | 1D array*) -- Lithium ion diffusivity in the electrolyte [m^2/s].


   .. py:method:: get_gamma(C_Li, T)

      Calculate the electrolyte thermodynamic factor at concentration
      ``C_Li`` and temperature ``T``.

      :param C_Li: Lithium ion concentration in the electrolyte [kmol/m^3].
      :type C_Li: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **gamma** (*float | 1D array*) -- Thermodynamic factor [-].


   .. py:method:: get_kappa(C_Li, T)

      Calculate the electrolyte conductivity at concentration ``C_Li`` and
      temperature ``T``.

      :param C_Li: Lithium ion concentration in the electrolyte [kmol/m^3].
      :type C_Li: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **kappa** (*float | 1D array*) -- Electrolyte conductivity [S/m].


   .. py:method:: get_t0(C_Li, T)

      Calculate the lithium ion transference number at concentration ``C_Li``
      and temperature ``T``.

      :param C_Li: Lithium ion concentration in the electrolyte [kmol/m^3].
      :type C_Li: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **t0** (*float | 1D array*) -- Lithium ion transference number [-].



