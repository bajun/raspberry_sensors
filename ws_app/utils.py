""" Project utils """

from typing import Dict

import yaml


def load_config(fname: str) -> Dict:
    """
    Import configs from file
    :param fname: filename
    :return:
    """
    with open(fname, "rt") as file:
        data = yaml.safe_load(file)
    return data
