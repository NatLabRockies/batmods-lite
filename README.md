# BatMods-LitePINNSTRIPES [![BATMODS-LITE-CI](https://github.com/NREL/BatMods-lite/actions/workflows/ci.yml/badge.svg)](https://github.com/NREL/BatMods-lite/actions/workflows/ci.yml) 

## Installing

## Quick start

## Formatting [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Code formatting and import sorting are done automatically with `black` and `isort`. 

## Acknowledgements
This work was authored by the National Renewable Energy Laboratory (NREL), operated by Alliance for Sustainable Energy, LLC, for the U.S. Department of Energy (DOE) under Contract No. DE-AC36-08GO28308. This work was supported by funding from DOE's Vehicle Technologies Office (VTO) and Advanced Scientific Computing Research (ASCR) program. The research was performed using computational resources sponsored by the Department of Energy's Office of Energy Efficiency and Renewable Energy and located at the National Renewable Energy Laboratory. The views expressed in the repository do not necessarily represent the views of the DOE or the U.S. Government.

## References




# BatMods-lite (Battery Models - lite)
BatMods-lite is a Python package that includes:

1) Pre-built battery models
2) Kinetic/transport properties for common battery materials

# Installing
It is highly recommended to use [Anaconda](https://www.anaconda.com/download)
to create and manage your Python virtual environments. The following directions
assume you are using Anaconda. At the moment, no support is provided for alternate
methods. 

After installing Anaconda, open Anaconda Prompt (Windows) or Terminal (MacOS)
and run the following to: (1) create an environment named "batmods," (2) activate
your new environment, (3) install scikits-odes, (4) install batmods-lite. 

1) ``conda create -n batmods python=3.10``
2) ``conda activate batmods``
3) ``conda install scikits.odes``
4) ``pip install ./batmods-lite`` or ``pip install -e ./batmods-lite``

**Notes:**
----------
* scikits-odes is installed separately through ``conda install`` rather than
``pip install`` because it is built off C++ and Fortran code. Installing via 
``pip`` would complicated the setup because it requires additional compilers 
and packages to be installed beforehand. 

* Step (4) assumes your current working directory is where you haved saved
the BatMods-lite package. The package is not currently hosted on PyPI and must
be installed from a local directory.

* The ``-e`` flag in step (4) should be used if you plan to make changes to the
local package. This installs the package in "editable" mode. 

# Get Started
You are now ready to start running models. Documentation is available within the
package itself. Run the following from your favorite terminal/IDE to see examples
and more:

```python
import bmlite as bm

bm.docs()
```

