import json
import time
from pathlib import Path


def write_to_json(_dir: str, filename: str, data, mode='w'):
    Path(_dir).mkdir(parents=True, exist_ok=True)
    with open(f'{_dir}/{filename}', mode) as f:
        json.dump(data, f)


def read_json(file_path: str):
    f = open(file_path, encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


def convert_strftime(timestamp, time_format='%d/%m/%Y'):
    datetime = time.strftime(time_format, time.localtime(timestamp))
    return datetime
