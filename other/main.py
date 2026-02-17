# import ast

# file1 = input("Enter filepath-1:")
# file2 = input("Enter filepath-2:")

# # file_path = 'your_file.txt' # Make sure to use the correct path to your file

# try:
#     with open(file1, 'r') as file:
#         content1 = file.read()
#     print(content1)
# except FileNotFoundError:
#     print(f"Error: The file '{file1}' was not found.")
# except Exception as e:
#     print(f"An error occurred: {e}")

# try:
#     with open(file2, 'r') as file:
#         content2 = file.read()
    
#     print(content2)
# except FileNotFoundError:
#     print(f"Error: The file '{file1}' was not found.")
# except Exception as e:
#     print(f"An error occurred: {e}")


# tree1 = ast.parse(content1, filename='<ast>', mode='exec')
# # For debugging and inspection
# print(ast.dump(tree1, indent=4))
# tree2 = ast.parse(content2, filename='<ast>', mode='exec')
# # For debugging and inspection
# print(ast.dump(tree2, indent=4))


import ast
from difflib import SequenceMatcher


# ==============================
# STEP 1: AST Normalization
# ==============================

# Ignore nodes that change in Type-2 plagiarism
IGNORE_NODES = {"Name", "Constant", "Load", "Store", "Del"}


def extract_structure(node):
    """
    Extract ordered AST node types (preorder traversal)
    while ignoring identifiers and literals.
    """
    structure = []

    node_type = type(node).__name__

    # Filter out irrelevant nodes
    if node_type not in IGNORE_NODES:
        structure.append(node_type)

    # Traverse children in order
    for child in ast.iter_child_nodes(node):
        structure.extend(extract_structure(child))

    return structure


def get_ast_signature(code):
    """
    Generate structural signature of code.
    """
    try:
        tree = ast.parse(code)
        return extract_structure(tree)
    except SyntaxError:
        return []


# ==============================
# STEP 2: Similarity Computation
# ==============================

def compute_similarity(code1, code2):
    """
    Compute similarity score between two programs.
    """
    sig1 = get_ast_signature(code1)
    sig2 = get_ast_signature(code2)

    return SequenceMatcher(None, sig1, sig2).ratio()


# ==============================
# STEP 3: Plagiarism Decision
# ==============================

def detect_plagiarism(code1, code2, threshold=0.8):
    """
    Detect Type-2 plagiarism based on threshold.
    """
    score = compute_similarity(code1, code2)

    print("AST Signature 1:", get_ast_signature(code1))
    print("AST Signature 2:", get_ast_signature(code2))
    print(f"Similarity Score: {score:.3f}")

    if score >= threshold:
        print("Result: Potential Type-2 plagiarism detected.")
    else:
        print("Result: Not Type-2 plagiarism.")


# ==============================
# STEP 4: Example Test
# ==============================

if __name__ == "__main__":

#     code1 = """
# def add(a, b):
#     return a + b
# """

#     code2 = """
# def sum_values(x, y):
#     return x + y
# """
    file1 = input("Enter filepath-1:")
    file2 = input("Enter filepath-2:")

    # file_path = 'your_file.txt' # Make sure to use the correct path to your file

    try:
        with open(file1, 'r') as file:
            code1 = file.read()
        # print(content1)
    except FileNotFoundError:
        print(f"Error: The file '{file1}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        with open(file2, 'r') as file:
            code2 = file.read()
        
        # print(content2)
    except FileNotFoundError:
        print(f"Error: The file '{file1}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    detect_plagiarism(code1, code2)
