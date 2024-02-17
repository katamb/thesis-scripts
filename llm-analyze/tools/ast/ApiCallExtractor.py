from tree_sitter import Language, Parser
import re

JAVA_LANGUAGE = Language('tools/ast/build/my-languages.so', 'java')
parser = Parser()
parser.set_language(JAVA_LANGUAGE)


class JavaApiExtractor:
    def __init__(self):
        self.api_sequence = []
        self.variable_types = {}

    def try_removing_idx(self, object_name):
        pattern = r'\[\d+\]'
        clean_obj_name = re.sub(pattern, '', object_name)
        if clean_obj_name in self.variable_types:
            return self.variable_types.get(clean_obj_name)
        return None

    def parse_code(self, code):
        tree = parser.parse(bytes(code, "utf8"))
        self.build_variable_type_map(tree.root_node)  # First pass to build the map
        self.walk_tree(tree.root_node)  # Second pass

    def build_variable_type_map(self, node):
        if node.type == 'variable_declarator':
            # Assuming the parent is a variable declaration with type information
            variable_type = node.parent.child_by_field_name('type').text.decode('utf-8')
            variable_name = node.child_by_field_name('name').text.decode('utf-8')
            self.variable_types[variable_name] = variable_type
        if node.type == 'formal_parameter':
            variable_type = node.child_by_field_name('type').text.decode('utf-8')
            variable_name = node.child_by_field_name('name').text.decode('utf-8')
            self.variable_types[variable_name] = variable_type

        # Continue scanning all children nodes
        for child in node.children:
            self.build_variable_type_map(child)

    def extract_class_name(self, java_constructor):
        pattern = r'new\s+([\w.]+)\s*\('
        match = re.search(pattern, java_constructor)
        if match:
            return match.group(1)
        else:
            return None

    def walk_tree(self, node):
        for child in node.children:
            self.walk_tree(child)

        if node.type == 'method_invocation':
            self.handle_method_invocation(node)
        elif node.type == 'object_creation_expression':
            self.handle_object_creation_expression(node)

    def handle_method_invocation(self, node):
        method_name = node.child_by_field_name('name').text.decode('utf-8')
        # Extract name of the variable or object this method is called on
        object_node = node.child_by_field_name('object')
        if object_node:
            object_name = object_node.text.decode('utf-8')
            method_class = self.variable_types.get(object_name)
            if method_class is None:
                method_class = self.try_removing_idx(object_name)
            if method_class is None:  # This needs changes to be more flexible, but was enough for current dataset
                method_class = self.extract_class_name(object_name)
            if method_class is None:
                method_class = node.children[0].text.decode("utf-8")

            self.api_sequence.append(f"{method_class}.{method_name}")

    def handle_object_creation_expression(self, node):
        class_name = node.child_by_field_name('type').text.decode('utf-8')
        self.api_sequence.append(f'{class_name}.new')

    def get_api_sequence(self):
        return '->'.join(self.api_sequence)


def get_api_call_seq(code):
    extractor = JavaApiExtractor()
    extractor.parse_code(code)
    seq = extractor.get_api_sequence()
    print("API sequence:", seq)
    return seq
