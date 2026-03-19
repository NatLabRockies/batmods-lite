Project Layout
==============
The `BATMODS-lite` project is organized to provide clarity and structure, making it easy for developers to navigate and contribute. Below is an outline of the key directories and files, along with guidelines for working within them.

Root Directory
--------------
The root directory contains the most important files and folders necessary for development:

* **src/:** The core package code resides in this directory. This is the primary folder developers will interact with when modifying or adding features.
* **pyproject.toml:** This file contains the project's build system configurations and dependencies. If you need to add or modify dependencies, you should do so in this file.
* **noxfile.py:** Contains automation scripts for tasks like testing, linting, formatting, and building documentation. Developers should use nox sessions as needed to ensure code quality and consistency.
* **tests/:** This is where all unit tests and integration tests are stored. Any new functionality should include appropriate tests here.
* **docs/:** Contains documentation files for the project. Developers contributing to the documentation should work here, particularly if adding or improving developer guides or API references.

Source Directory
----------------
The `src/` directory contains the main package code. Using this structure ensures that local imports during development come from the installed package rather than accidental imports from the source files themselves.

Top-level Package
^^^^^^^^^^^^^^^^^
The core classes/functions of the `BATMODS-lite` package reside within the `_core` directory and include the solvers and experiment definitions used across all models. Each model is defined within its own subdirectory, e.g., `SPM` and `P2D`. Additional functionality that is shared across models is organized into either a subpackage or submodule, dependings on the size and complexity of the code. The main classes/functions in the top-level package include:

* `Constants`: A class that contains all the physical constants used across the models. This ensures consistency and ease of maintenance when updating or adding new constants.
* `Experiment`: Manages input experiments for simulations. The class supports dynamic or static load profiles and/or limiting criteria, similar to a laboratory cycler.
* `IDASolver`: A class that provides an interface to the IDA solver from the Sundials suite. This is the default solver for all models and is designed to be flexible and user-friendly.
* `templates`: A function that helps users find and print templates for the different models. This is especially useful for new users who want to quickly get started with the package without having to read through extensive documentation first.

Each of these classes/functions typically resides in its own file, following a philosophy of keeping files manageable in size. If multiple classes or functions share significant overlap in purpose, they may be grouped in the same file, but care is taken to keep files concise and easy to navigate.

Subpackages
^^^^^^^^^^^
There are multiple submodules/subpackages that handle specific functionality. For example:

* `materials`: Contains classes for electrode active material and electrolyte material properties. These can be used across all models and are organized in a way that allows for easy extension as new materials are added to the package.
* `mesh`: Provides routines to build the spatial meshes for the different models. Also includes functions to generate corresponding pointers, i.e., integer arrays that identify where specific state variables are located within a solution vector.
* `SPM`: Contains the Single Particle Model (SPM) implementation, including all related classes, functions, and utilities specific to this model.
* `P2D`: Contains the Pseudo-Two-Dimensional (P2D) model implementation, including all related classes, functions, and utilities specific to this model.

This list is not exhaustive, and the structure may evolve as the project grows. The key principle is to organize code in a way that promotes modularity and ease of maintenance, while also ensuring that related functionality is grouped together logically. Additionally, note that model subpackages use a consistent structure and naming convention (capitalized names) compared to other subpackages and submodules (lowercase names). This is intentional to help users quickly identify where the different models are located within the package.
