from collections import defaultdict
from typing import Any, Optional


class Parameter:
    def __init__(self, name: str, value: Any, required: bool = True):
        self.name = name
        self.value = value
        self.required = required


def reverse_lookup(mapping: dict[str, Parameter]) -> defaultdict:
    reverse_mapping = defaultdict(list)
    for key, param in mapping.items():
        if param.required:
            reverse_mapping[param.value].append(key)
    return reverse_mapping


def parse_string_inputs(input_value: Optional[str] = None):
    stripped = input_value.strip()
    if stripped:
        return stripped
    return None


def parse_integer_inputs(input_value: Optional[str] = None):
    if input_value:
        return max(0, int(input_value))
    return None


def describe_parameters(user_parameters: dict[str, Parameter]):
    description: dict[str, str] = dict()
    for key, param in user_parameters.items():
        description[key] = param.value
    return description
