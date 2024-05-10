import argparse
import ast
import glob
import os

import astor


class ReplaceFuncs(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.parent_stack = []  # Stack to keep track of parent nodes

    def visit_ClassDef(self, node):
        """Visit a class definition and process its methods."""
        self.parent_stack.append(node)  # Push the class onto the parent stack
        for n in node.body:
            self.visit(n)  # Manually visit each node within the class body
        self.parent_stack.pop()  # Pop the class off the parent stack after processing its body
        return node

    def visit_FunctionDef(self, node):
        """Visit function definitions and remove specified decorators."""
        in_class = any(isinstance(parent, ast.ClassDef) for parent in self.parent_stack)
        if any(
            isinstance(decorator, ast.Name) and decorator.id == "mark_student_function"
            for decorator in node.decorator_list
        ):
            docstring = ast.get_docstring(node)

            node.body = [ast.Raise(ast.Name("NotImplementedError", ast.Load()))]
            node.decorator_list = [
                decorator
                for decorator in node.decorator_list
                if decorator.id != "mark_student_function"
            ]

            if docstring:
                tab_indent = "\t"
                if in_class:
                    tab_indent += "\t"

                docstring_lines = docstring.splitlines()
                if docstring_lines:
                    docstring_lines[0] = f"\n{tab_indent}" + docstring_lines[0]
                docstring_lines.append("")
                docstring_lines = [f"{tab_indent}{line}" for line in docstring_lines]
                docstring_node = ast.Expr(value=ast.Str(s="\n".join(docstring_lines)))
                node.body.insert(0, docstring_node)
        return node


def process_file(file_path, input_dir, output_dir):
    """Process a single file, applying transformations."""
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    ReplaceFuncs().visit(tree)

    relative_path = os.path.relpath(file_path, start=input_dir)
    new_file_path = os.path.join(output_dir, relative_path)
    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

    with open(new_file_path, "w") as new_file:
        new_file.write(astor.to_source(tree))

    print(f"Processed file saved as: {new_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process Python files to remove specified decorators."
    )
    parser.add_argument(
        "--input_path",
        required=True,
        help="Directory containing Python files to process.",
    )
    parser.add_argument(
        "--output_path", required=True, help="Directory to save processed files."
    )
    args = parser.parse_args()

    for file_path in glob.glob(args.input_path + "/**/*.py", recursive=True):
        if "mark_student_functions" not in file_path:
            process_file(file_path, args.input_path, args.output_path)
