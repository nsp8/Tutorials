from copy import deepcopy
from re import search
from pathlib import Path
from time import sleep


def delay(function):
    def wrapper(*args, **kwargs):
        sleep(3)
        result = function(*args, **kwargs)
        sleep(2)
        return result
    return wrapper


def update_contents(old: dict, new: dict):
    reconciled = deepcopy(old)
    for k, v in new.items():
        if k in old:
            reconciled[k]["contents"].extend(new[k]["contents"])
        else:
            reconciled[k] = new[k]
    return reconciled


def get_latest_file_version(file_path):
    versions = list()
    pattern = r"_?(\d+)\.json"
    for f in file_path.iterdir():
        if Path.match(f, r"*.json"):
            try:
                version = search(pattern, f.name).groups()[0]
                if version:
                    versions.append(int(version))
            except (AttributeError, TypeError, ValueError):
                pass
    return max(versions) if versions else 0
