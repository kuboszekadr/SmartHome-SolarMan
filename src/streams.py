import os
import json


def stream_to_disk(data, root: str, data_date: str):
    file_path = os.path.join(root, f'{data_date}.json')

    with open(file_path, 'w') as f:
        json.dump(data, f)


def stream_to_api(data):
    raise NotImplementedError
