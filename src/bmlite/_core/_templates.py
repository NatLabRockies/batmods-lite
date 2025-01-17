import os
import json
from pathlib import Path

from ruamel.yaml import YAML


def _templates(model__file__: str, model_name: str, sim: str | int = None,
               exp: str | int = None) -> None:
    """
    Print simulation and/or experiment templates. If both ``sim`` and ``exp``
    are ``None``, a list of available templates will be printed. Otherwise,
    if a name or index is given, that template will print to the console.

    Parameters
    ----------
    model__file__ : str
        The module ``__file__`` attribute. This sets the local path to make
        sure templates are pulled from the correct model path.
    model_name : str
        Name for the model package. This ensures template lists are labeled
        correctly.
    sim : str | int, optional
        Simulation template file name or index. The default is ``None``.
    exp : str | int, optional
        Experiment template file name or index. The default is ``None``.

    Returns
    -------
    None.

    """

    dirname = os.path.dirname(model__file__)

    simlist = os.listdir(dirname + '/default_sims/')
    explist = os.listdir(dirname + '/default_exps/')

    if sim is None and exp is None:
        print('\nTemplates for ' + model_name + ' simulations:')
        for i, file in enumerate(simlist):
            print('- [' + str(i) + '] ' + file.removesuffix('.yaml'))

        print('\nTemplates for ' + model_name + ' experiments:')
        for i, file in enumerate(explist):
            print('- [' + str(i) + '] ' + file.removesuffix('.yaml'))

    if isinstance(sim, str):
        if '.yaml' not in sim:
            sim += '.yaml'

        simfile = sim
    elif isinstance(sim, int):
        simfile = simlist[sim]

    if sim is not None:
        print('\n' + '=' * 30 + '\n' + simfile + '\n' + '=' * 30)
        with open(dirname + '/default_sims/' + simfile, 'r') as f:
            print('\n' + f.read())

    yaml = YAML()

    if isinstance(exp, str):
        if '.yaml' not in exp:
            exp += '.yaml'

        expfile = exp
    elif isinstance(exp, int):
        expfile = explist[exp]

    if exp is not None:
        print('\n' + '=' * 30 + '\n' + expfile + '\n' + '=' * 30)
        expdict = yaml.load(Path(dirname + '/default_exps/' + expfile))
        print('exp = ' + json.dumps(expdict, indent=4))
