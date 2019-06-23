import json
import os
from contextlib import contextmanager

SECRET_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'secret', 'secret.txt')
STATE_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'secret', 'state.json')


def read_secret(secret):
    """
    Reads a secret from the module level SECRET_FILE_NAME

    :param str secret:
    :rtype: str
    """
    with open(SECRET_FILE_NAME, 'r') as f:
        lines = list(filter(lambda line: not line.startswith('#') and line and secret in line, f.readlines()))

    return lines[0].partition('=')[2].strip()


@contextmanager
def manage_state():
    """
    Reads the full state from module level STATE_FILE_NAME

    Yields the state as a JSON object (dictionary or list) and saves the modified state on exit
    """
    with open(STATE_FILE_NAME, 'r') as f:
        data = json.load(f)
    yield data  # since we're passing the object we create here, changes propagate back
    with open(STATE_FILE_NAME, 'w') as f:
        f.write(json.dumps(data, sort_keys=True, indent=2))
