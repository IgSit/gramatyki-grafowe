import os
import numpy as np
from PIL import Image
import copy
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


def get_current_file_directory():
    return os.path.dirname(os.path.abspath(__file__))

def create_test_directory(base_dir, sub_dir):
    test_dir = os.path.join(base_dir, sub_dir)
    os.makedirs(test_dir, exist_ok=True)
    return test_dir


def apply_production(graph, production):
    hyper_nodes_copy = copy.deepcopy(graph.hyper_nodes)
    processed_hyper_nodes = []
    
    while hyper_nodes_copy:
        for hyper_node in hyper_nodes_copy:
            if hyper_node in processed_hyper_nodes:
                continue
            
            processed_hyper_nodes.append(hyper_node)
            if production.check(graph, hyper_node):
                graph = production.apply(graph, hyper_node)
                hyper_nodes_copy = copy.deepcopy(graph.hyper_nodes)
                break
            
        else:
            break
    
    return graph


def compare_with_baseline(buffer, baseline_path):
    if os.path.exists(baseline_path):
        with open(baseline_path, "rb") as f:
            baseline_image = Image.open(f)
            test_image = Image.open(buffer)
            return compare_images(baseline_image, test_image)
    else:
        with open(baseline_path, "wb") as f:
            f.write(buffer.getvalue())
        return True


def compare_images(img1, img2):
    img1_array = np.array(img1, dtype=np.int16)
    img2_array = np.array(img2, dtype=np.int16)

    difference = np.abs(img1_array - img2_array)
    return not np.any(difference > 5)
