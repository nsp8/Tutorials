from copy import deepcopy
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
