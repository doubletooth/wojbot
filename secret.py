import json
import os
from contextlib import contextmanager

SECRET_FILE_NAME = os.path.join(os.path.dirname(__file__), 'secret.txt')
STATE_FILE_NAME = os.path.join(os.path.dirname(__file__), 'state.json')


def read_secret(secret):
    with open(SECRET_FILE_NAME, 'r') as f:
        lines = filter(lambda line: not line.startswith('#') and line and secret in line, f.readlines())

    assert len(lines) == 1, 'Found more than one secret in file!'
    return lines[0].partition('=')[2].strip()


@contextmanager
def manage_state():
    with open(STATE_FILE_NAME, 'r') as f:
        data = json.load(f)
    yield data
    with open(STATE_FILE_NAME, 'w') as f:
        f.write(json.dumps(data, sort_keys=True, indent=4))
