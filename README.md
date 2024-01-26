<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./images/dark.svg">
  <img alt="BatMods-lite logo" src="./images/light.svg">
</picture> 

[![CI][ci-b]][ci-l] ![tests][test-b] ![coverage][cov-b] [![pep8][pep-b]][pep-l]

[ci-b]: https://github.com/NREL/BatMods-lite/actions/workflows/ci.yaml/badge.svg
[ci-l]: https://github.com/NREL/BatMods-lite/actions/workflows/ci.yaml

[test-b]: ./images/tests.svg
[cov-b]: ./images/coverage.svg

[pep-b]: https://img.shields.io/badge/code%20style-pep8-orange.svg
[pep-l]: https://www.python.org/dev/peps/pep-0008

BatMods-lite is a Python package that includes: 

1) A library and API for pre-built battery models
2) Kinetic/transport properties for common battery materials

## Installing
We recommend using [Anaconda](https://www.anaconda.com/download) to create and manage your Python virtual environments. The following directions assume you are using Anaconda. 

After downloading or cloning the BatMods-lite repo files onto your local machine, open Anaconda Prompt (Windows) or Terminal (MacOS/Linux) and run the following to: (1) create an environment named "batmods," (2) activate your new environment, (3) install scikits.odes, and (4) install batmods-lite. 

1) ``conda create -n batmods python=3.10``
2) ``conda activate batmods``
3) ``conda install scikits.odes``
4) ``pip install .`` or ``pip install -e .``

**Notes:**
* You can replace "batmods" in steps (1) and (2) with your preferred environment name.

* Step (3) installs scikits.odes separately using  ``conda install`` on purpose. Installing scikits.odes via ``pip`` complicates the setup by requiring extra pre-installed softwares and compilers, as covered in the [scikits.odes documenation](https://scikits-odes.readthedocs.io/en/latest/).

* The ``-e`` flag in step (4) installs BatMods-lite in "editable" mode. Use this if you plan to make changes to the package.

* The path in step (4) assumes you already used ``cd`` to move into the directory that includes the BatMods-lite "setup.py" file. If this is not true, please ``cd`` into the correct directory, or change the path accordingly.

## Get Started
You are now ready to start running models. Run the following from your favorite terminal/IDE to see helpful documentation, examples, and more:

```python
import bmlite as bm

bm.docs()
```

Or, run the following mini script to simulate the default single particle model (SPM) in a constant 2C discharge experiment for 1350 seconds. The returned solution ``sol`` includes post processing/plotting methods. The final line below plots the current, voltage, and power vs. time.

```python
import bmlite as bm

sim = bm.SPM.Simulation()

exp = {'C_rate': -2.0, 
       't_min': 0.0,
       't_max': 1350.0,
       'Nt': 150
       }

sol = sim.run_CC(exp)
sol.plot('ivp')
```

**Notes:**
* If you are new to Python, check out [Spyder IDE](https://www.spyder-ide.org/). Spyder is a powerful interactive development environment (IDE). BatMods-lite is programmed almost entirely using the Spyder IDE. 

* You can install Spyder using ``conda install spyder``. Afterward, you can find the application on your system, or run ``spyder`` in Anaconda Prompt or Terminal to open an instance.

## Formatting
BatMods-lite code mostly follows the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008). However, we allow adding extra spaces around parentheses or brackets, and under- or over-indenting multi-line expressions when it improves readability or avoids the 80-character line limit. 

Be aware that it is the authors' preference to not adopt the more opinionated [black formatting style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html). Please avoid autoformatting any files in this style if you plan to contribute.

## Acknowledgements
This work was authored by the National Renewable Energy Laboratory (NREL), operated by Alliance for Sustainable Energy, LLC, for the U.S. Department of Energy (DOE) under Contract No. DE-AC36-08GO28308. This work was supported by funding from DOE's Vehicle Technologies Office (VTO) and Advanced Scientific Computing Research (ASCR) program. The research was performed using computational resources sponsored by the Department of Energy's Office of Energy Efficiency and Renewable Energy and located at the National Renewable Energy Laboratory. The views expressed in the repository do not necessarily represent the views of the DOE or the U.S. Government.
