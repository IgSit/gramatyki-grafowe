import os
import numpy as np
from PIL import Image
import copy

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
    img1_array = np.array(img1)
    img2_array = np.array(img2)

    difference = np.abs(img1_array - img2_array)
    return not np.any(difference > 5)
