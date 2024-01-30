from tree_sitter import Language, Parser
from langchain.agents import tool
import os
import uuid

JAVA_LANGUAGE = Language("ast/build/my-languages.so", "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)


@tool("Get AST for Java code")
def get_ast_from_file(file_path):
    """Tool that returns the abstract syntax tree (AST) of Java code when given the location of the Java file."""
    with open(file_path, "r") as f:
        code = f.read()
    get_ast_from_code(code)


@tool("Get AST for Java code")
def get_ast_from_code(code):
    """Tool that returns the abstract syntax tree (AST) of given Java code snippet."""
    tree = parser.parse(bytes(code, "utf8"))
    generated_name = "./ast/" + str(uuid.uuid4())
    with open(generated_name, "w") as f:
        f.write("")

    traverse_tree(tree.root_node, generated_name)
    with open(generated_name, "r") as f:
        result = f.read()
    os.remove(generated_name)
    print(result)
    return result


# Traverse the syntax tree
def traverse_tree(node, generated_name, depth=0):
    if node.is_named:
        with open(generated_name, "a") as f:
            f.write("|" + "-" * depth + f"{node.type} [lines: {node.start_point[0] + 1}-{node.end_point[0] + 1}]\n")

    for child in node.children:
        traverse_tree(child, generated_name, depth + 1)
