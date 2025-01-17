import os


def _templates(model__file__: str, model_name: str,
               sim: str | int = None) -> None:
    """
    Print simulation templates. If ``sim`` is ``None``, a list of available
    templates will be printed. Otherwise, if a name or index is given, that
    template will print to the console.

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

    Returns
    -------
    None.

    """

    dirname = os.path.dirname(model__file__)

    simlist = os.listdir(dirname + '/default_sims/')

    if sim is None:
        print('\nTemplates for ' + model_name + ' simulations:')
        for i, file in enumerate(simlist):
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
