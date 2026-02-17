import ast
from difflib import SequenceMatcher
import numpy as np

IGNORE_NODES = {"Name", "Constant", "Load", "Store", "Del"}


def extract_structure(node):
    structure = []
    node_type = type(node).__name__

    if node_type not in IGNORE_NODES:
        structure.append(node_type)

    for child in ast.iter_child_nodes(node):
        structure.extend(extract_structure(child))

    return structure


def get_ast_signature(code):
    try:
        tree = ast.parse(code)
        return extract_structure(tree)
    except:
        return []


def compute_similarity(code1, code2):
    sig1 = get_ast_signature(code1)
    sig2 = get_ast_signature(code2)
    return SequenceMatcher(None, sig1, sig2).ratio()


def pairwise_similarity(programs):
    files = list(programs.keys())
    n = len(files)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            score = compute_similarity(programs[files[i]], programs[files[j]])
            matrix[i][j] = score
            matrix[j][i] = score

    return files, matrix
