import re


def prepare_edges(input_dict) -> dict:
    """
    Ignores numbering of hyper-nodes (order of creation does not matter for X{n}).
    Sorts all edges since they are not directed.
    :param input_dict:
    :return:
    """
    def shift_label(label):
        if isinstance(label, str) and re.match(r'^X\d+$', label):
            return 'X'
        return label

    def normalize_edges(raw_dict: dict):
        normalized_dict = {}
        for k, v in raw_dict.items():
            if isinstance(k, tuple):
                normalized_key = tuple(sorted(k))
            else:
                normalized_key = k
            normalized_dict[normalized_key] = v
        return normalized_dict

    shifted_dict = {}
    for key, value in input_dict.items():
        shifted_key = tuple(shift_label(part) for part in key)
        shifted_value = shift_label(value)
        shifted_dict[shifted_key] = shifted_value

    return normalize_edges(shifted_dict)
