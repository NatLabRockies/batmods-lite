:py:mod:`bmlite.P2D.builder`
============================

.. py:module:: bmlite.P2D.builder

.. autoapi-nested-parse::

   .. rubric:: Battery Builder

   Contains classes to construct the battery for P2D simulations. Each class reads
   in keyword arguments that define parameters relevant to its specific domain.
   For example, the area and temperature are ``Battery`` level parameters because
   they are the same everywhere, but the discretizations ``Nx`` and ``Nr`` may be
   different for the anode, separator, and cathode domains.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   bmlite.P2D.builder.Battery
   bmlite.P2D.builder.Electrode
   bmlite.P2D.builder.Electrolyte
   bmlite.P2D.builder.Separator




.. py:class:: Battery(**kwargs)




   
   A class for battery-level attributes.

   :param \*\*kwargs: Keyword arguments to set the battery-level attributes. The required
                      keys and descriptions are given below:

                      ====== =====================================================
                      Key    Description [units] (type)
                      ====== =====================================================
                      cap    nominal battery capacity [A*h] (*float*)
                      temp   temperature [K] (*float*)
                      area   area normal to the current collectors [m^2] (*float*)
                      ====== =====================================================
   :type \*\*kwargs: dict, required

   .. py:method:: update()

      Updates any secondary/dependent parameters. At present, this method
      does not do anything for the ``Battery`` class.

      :returns: *None.*



.. py:class:: Electrode(**kwargs)




   
   A class for the electrode-specific attributes and methods.

   This class is used to build both the anode and cathode for P2D
   simulations.

   :param \*\*kwargs: Keyword arguments to set the electrode attributes. The required
                      keys and descriptions are given below:

                      ========= =========================================================
                      Key       Description [units] (type)
                      ========= =========================================================
                      Nx        number of ``x`` discretizations [-] (*int*)
                      Nr        number of ``r`` discretizations [-] (*int*)
                      thick     electrode thickness [m] (*float*)
                      R_s       represenatative particle radius [m] (*float*)
                      eps_el    electrolyte volume fraction [-] (*float*)
                      eps_CBD   carbon binder domain volume fraction [-] (*float*)
                      p_sol     solids Bruggeman factor, ``eps_s**p_sol`` [-] (*float*)
                      p_liq     liquids Bruggeman factor, ``eps_el**p_liq`` [-] (*float*)
                      alpha_a   Butler-Volmer anodic symmetry factor [-] (*float*)
                      alpha_c   Butler-Volmer cathodic symmetry factor [-] (*float*)
                      Li_max    max solid-phase lithium concentraion [kmol/m^3] (*float*)
                      x_0       initial solid-phase intercalation fraction [-] (*float*)
                      i0_deg    ``i0`` degradation factor [-] (*float*)
                      Ds_deg    ``Ds`` degradation factor [-] (*float*)
                      material  class name from ``bmlite.materials`` [-] (*str*)
                      ========= =========================================================
   :type \*\*kwargs: dict, required

   .. py:method:: algidx() -> numpy.ndarray


   .. py:method:: get_Ds(x: float | numpy.ndarray, T: float) -> float | numpy.ndarray

      Calculate the lithium diffusivity in the solid phase given the local
      intercalation fraction ``x`` and temperature ``T``.

      :param x: Lithium intercalation fraction [-].
      :type x: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **Ds** (*float | 1D array*) -- Lithium diffusivity in the solid phase [m^2/s].


   .. py:method:: get_Eeq(x: float | numpy.ndarray, T: float) -> float | numpy.ndarray

      Calculate the equilibrium potential given the surface intercalation
      fraction ``x`` at the particle surface and temperature ``T``.

      :param x: Lithium intercalation fraction at ``r = R_s`` [-].
      :type x: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **Eeq** (*float | 1D array*) -- Equilibrium potential [V].


   .. py:method:: get_i0(x: float | numpy.ndarray, C_Li: float | numpy.ndarray, T: float) -> float | numpy.ndarray

      Calculate the exchange current density given the surface intercalation
      fraction ``x`` at the particle surface, the local lithium ion
      concentration ``C_Li``, and temperature ``T``. The input types for
      ``x`` and ``C_Li`` should both be the same (i.e., both float or both
      1D arrays).

      :param x: Lithium intercalation fraction at ``r = R_s`` [-].
      :type x: float | 1D array
      :param C_Li: Lithium ion concentration in the local electrolyte [kmol/m^3].
      :type C_Li: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **i0** (*float | 1D array*) -- Exchange current density [A/m^2].


   .. py:method:: make_mesh() -> None

      Determines/sets the ``x`` locations for all of the "minus" interfaces
      ``xm``, "plus" interfaces ``xp``, and control volume centers ``x``
      based on the electrode thickness and ``Nx`` discretization. At present,
      only a uniform mesh is supported.

      Also determines/sets the ``r`` locations for all of the "minus"
      interfaces ``rm``, "plus" interfaces ``rp``, and control volume centers
      ``r`` based on the representative particle radius and ``Nr``
      discretization. At present, only a uniform mesh is supported.

      :returns: *None.*

      .. rubric:: Notes

      * "Minus" and "plus" interfaces represent the locations halfway between
        two control volume centers.
      * For a ``x`` control volume ``i``, ``xm_i < x_i`` and ``x_i < xp_i``.
      * For a ``r`` control volume ``j``, ``rm_j < r_j`` and ``r_j < rp_j``.


   .. py:method:: make_ptr() -> None


   .. py:method:: sv_0(el: object) -> numpy.ndarray


   .. py:method:: update() -> None

      Updates any secondary/dependent parameters. For the ``Electrode``
      class, this initializes the material class, and sets the following:

      * Solid-phase volume fraction [-]:
          ``eps_s = 1 - eps_el``
      * Activate material volume fraction [-]:
          ``eps_AM = 1 - eps_el - eps_CBD``
      * Solid-phase conductivity [S/m]:
          ``sigma_s = 10*eps_s``
      * Specific particle surface area [m^2/m^3]:
          ``A_s = eps_AM / R_s``

      :returns: *None.*


   .. py:method:: x_ptr(key: str, shift: int = 0) -> list[int]



.. py:class:: Electrolyte(**kwargs)




   
   A class for the electrolyte attributes and methods.

   :param \*\*kwargs: Keyword arguments to set the electrolyte attributes. The required
                      keys and descriptions are given below:

                      ========== ================================================
                      Key        Description [units] (type)
                      ========== ================================================
                      li_0       initial Li+ concentration [kmol/m^3] (*float*)
                      material   class name from ``bmlite.materials`` [-] (*str*)
                      ========== ================================================
   :type \*\*kwargs: dict, required

   .. py:method:: get_D(C_Li: float | numpy.ndarray, T: float) -> float | numpy.ndarray

      Calculate the lithium ion diffusivity in the electrolyte solution at
      concentration ``C_Li`` and temperature ``T``.

      :param C_Li: Lithium ion concentration in the electrolyte [kmol/m^3].
      :type C_Li: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **D** (*float | 1D array*) -- Lithium ion diffusivity in the electrolyte [m^2/s].


   .. py:method:: get_gamma(C_Li: float | numpy.ndarray, T: float) -> float | numpy.ndarray

      Calculate the electrolyte thermodynamic factor at concentration
      ``C_Li`` and temperature ``T``.

      :param C_Li: Lithium ion concentration in the electrolyte [kmol/m^3].
      :type C_Li: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **gamma** (*float | 1D array*) -- Thermodynamic factor [-].


   .. py:method:: get_kappa(C_Li: float | numpy.ndarray, T: float) -> float | numpy.ndarray

      Calculate the electrolyte conductivity at concentration ``C_Li`` and
      temperature ``T``.

      :param C_Li: Lithium ion concentration in the electrolyte [kmol/m^3].
      :type C_Li: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **kappa** (*float | 1D array*) -- Electrolyte conductivity [S/m].


   .. py:method:: get_t0(C_Li: float | numpy.ndarray, T: float) -> float | numpy.ndarray

      Calculate the lithium ion transference number at concentration ``C_Li``
      and temperature ``T``.

      :param C_Li: Lithium ion concentration in the electrolyte [kmol/m^3].
      :type C_Li: float | 1D array
      :param T: Battery temperature [K].
      :type T: float

      :returns: **t0** (*float | 1D array*) -- Lithium ion transference number [-].


   .. py:method:: update() -> None

      Updates any secondary/dependent parameters. For the ``Electrolyte``
      class, this only initializes the material class.

      :returns: *None.*



.. py:class:: Separator(**kwargs)




   
   A class for the separator attributes and methods.

   This class is used to build both the separator for P2D simulations.

   :param \*\*kwargs: Keyword arguments to set the separator attributes. The required
                      keys and descriptions are given below:

                      ======== =========================================================
                      Key      Description [units] (type)
                      ======== =========================================================
                      Nx       Number of ``x`` discretizations [-] (*int*)
                      thick    Electrode thickness [m] (*float*)
                      eps_el   Electrolyte volume fraction [-] (*float*)
                      p_liq    Liquids Bruggeman factor, ``eps_el**p_liq`` [-] (*float*)
                      ======== =========================================================
   :type \*\*kwargs: dict, required

   .. py:method:: algidx() -> numpy.ndarray


   .. py:method:: make_mesh() -> None

      Determines/sets the ``x`` locations for all of the "minus" interfaces
      ``xm``, "plus" interfaces ``xp``, and control volume centers ``x``
      based on the electrode thickness and ``Nx`` discretization. At present,
      only a uniform mesh is supported.

      :returns: *None.*

      .. rubric:: Notes

      * "Minus" and "plus" interfaces represent the locations halfway between
        two control volume centers.
      * For ``x`` control volume ``i``, ``xm_i < x_i`` and ``x_i < xp_i``.


   .. py:method:: make_ptr() -> None


   .. py:method:: sv_0(el: object) -> numpy.ndarray


   .. py:method:: update() -> None

      Updates any secondary/dependent parameters. For the ``Separator``
      class, this sets the following:

      * Solid-phase volume fraction [-]:
          ``eps_s = 1 - eps_el``

      :returns: *None.*


   .. py:method:: x_ptr(key: str, shift: int = 0) -> list[int]



