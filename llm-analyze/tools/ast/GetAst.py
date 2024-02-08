from tree_sitter import Language, Parser
import os

JAVA_LANGUAGE = Language("build/my-languages.so", "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)


def return_ast(file_path):
    with open(file_path, "r") as f:
        code = f.read()

    tree = parser.parse(bytes(code, "utf8"))
    generated_name = file_path.split("\\")[-1].split(".")[0] + "-temp"
    with open(generated_name, "w") as f:
        f.write("")

    traverse_tree(tree.root_node, generated_name)
    with open(generated_name, "r") as f:
        result = f.read()
    os.remove(generated_name)
    return result


# Traverse the syntax tree
def traverse_tree(node, generated_name, depth=0):
    if node.is_named:
        with open(generated_name, "a") as f:
            f.write("|" + "-" * depth + f"{node.type} [lines: {node.start_point[0] + 1}-{node.end_point[0] + 1}]\n")

    for child in node.children:
        traverse_tree(child, generated_name, depth + 1)
