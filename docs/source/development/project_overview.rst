Project Overview
================

Introduction
------------
`BATMODS-lite` is a Python package designed to provide efficient, flexible, and physically grounded battery models based on electrochemical principles. It focuses on reduced-order physics-based models, including the Single Particle Model (SPM) and the Pseudo-2D (P2D) model, enabling simulation of various batteries.

The package is built to bridge the gap between computational efficiency and physical accuracy. It allows users to simulate battery performance under a wide range of operating conditions while retaining key internal states such as concentration gradients and reaction kinetics. Whether you are studying degradation mechanisms, generating high-quality synthetic datasets, or integrating physics-based models into estimation frameworks, `BATMODS-lite` provides the tools to do so effectively.

Key Features
^^^^^^^^^^^^
* **Physics-Based Models:** Includes implementations of the Single Particle Model (SPM) and Pseudo-Two-Dimensional (P2D) model, capturing electrochemical dynamics beyond equivalent circuit approximations.
* **Flexible Parameterization:** Model parameters can depend on state variables such as concentration and temperature, enabling realistic representation of battery behavior.
* **Versatile Experiment Interface:** The API allows for intuitive and flexible simulation of any type of load, including constant and dynamic loads driven by current, voltage, and/or power.
* **Cross-platform Support:** Written in Python, the package runs on any platform that supports Python and is continuously tested across multiple Python versions.

Use Cases
---------
`BATMODS-lite` is designed for advanced modeling tasks where physical interpretability and internal state resolution are critical:

* **Electrochemical Analysis:** Study internal battery dynamics such as lithium diffusion, reaction kinetics, and electrolyte transport.
* **Synthetic Data Generation:** Produce physically consistent datasets for algorithm development, validation, and machine learning applications.
* **Model Validation and Benchmarking:** Compare reduced-order and full-order models under identical operating conditions.
* **Optimization and Design:** Wrap the models in optimization frameworks to explore design spaces or perform diagnostic parameter estimation.

Target Audience
---------------
`BATMODS-lite` is intended for researchers and engineers who require physically meaningful battery models:

* Electrochemical model development
* Battery diagnostics and degradation studies

Technology Stack
----------------
* **Language:** Python
* **Compatibility:** Runs on any hardware that supports Python. Multiple versions are supported.

Project Origins
---------------
`BATMODS-lite` was developed by researchers at the **National Laboratory of the Rockies (NLR)**. Originally, the package was created to support generating synthetic datasets for data-driven model development. In particular, creating high-quality surrogate models for Bayesian optimization and inverse parameter modeling. However, the models and tools provided in `BATMODS-lite` are broadly applicable to a wide range of battery modeling tasks, and the project has evolved to support a variety of use cases in the battery research community.

Contributions
-------------
The `BATMODS-lite` project is hosted and actively maintained on `GitHub <https://github.com/NatLabRockies/batmods-lite>`_. Developers interested in contributing are encouraged to review the Code structure and Workflow sections for detailed information on the branching strategy, code review process, and how to get involved. All contributions are welcome.
