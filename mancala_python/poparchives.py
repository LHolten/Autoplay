'''Population Archives. Custom library to handle saving and loading of the agent populations.'''

import pickle
from pathlib import Path
### import sys

root = Path(".")
archives = root / "population archives"


def write(obj, filename: str):
    """Saves the object in archives with filename.

    Arguments:
        obj {list of NeuralNetworkd} -- The object to save.
        filename {str} -- The name of the file. (should have ending .pkl)
    """

    with open(archives / filename, 'wb') as output:
        # print("WRITING",sys.getsizeof(obj))
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load(filename: str):
    """Loads the file with filename and returns the object inside.

    Arguments:
        filename {str} -- The name of the file. 

    Returns:
        list of NeuralNetworks -- The contents of the file.
    """

    with open(archives / filename, 'rb') as input:
        return pickle.load(input)
