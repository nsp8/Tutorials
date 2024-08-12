from collections import defaultdict


def reverse_lookup(mapping: dict):
    reverse_mapping = defaultdict(list)
    for key, value in mapping.items():
        reverse_mapping[value].append(key)
    return reverse_mapping
