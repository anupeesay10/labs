import re
import ast


class File:
    def __init__(self, file):
        self.file = file

    def file_structure(self):
        """Analyzes the file structure: lines, packages, classes, and top-level functions."""
        lines = 0
        packages = 0
        classes = 0
        functions = 0

        # Count non-empty lines
        for line in self.file:
            if line.strip():
                lines += 1

        self.file.seek(0)
        # Count imported packages
        for line in self.file:
            strline = line.strip()
            if strline.startswith('import ') or strline.startswith('from '):
                packages += 1

        self.file.seek(0)
        # Count class definitions
        for line in self.file:
            strline = line.strip()
            if strline.startswith('class '):
                classes += 1

        self.file.seek(0)
        # Count top-level functions (outside of any class)
        inside_class = False

        for line in self.file:
            stripped = line.strip()
            if stripped.startswith('class '):
                inside_class = True
            elif stripped.startswith('def ') and not inside_class:
                if line.startswith('def '):  # Ensure it's top-level (not indented)
                    functions += 1
            elif not stripped:  # Reset inside_class on an empty line
                inside_class = False

        self.file.seek(0)  # Reset the file pointer
        return {
            "Lines": lines,
            "Packages": packages,
            "Classes": classes,
            "Functions": functions,
        }

    def name_convention(self):
        """Check if class and function names follow naming conventions."""
        self.file.seek(0)
        incorrect_classes = []
        incorrect_functions = []

        for line in self.file:
            line = line.strip()
            if line.startswith("class "):
                class_name = line.split()[1].split('(')[0].strip(':')  # Remove trailing colon
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', class_name):  # Class names must start with uppercase
                    incorrect_classes.append(class_name)

            elif line.startswith("def "):
                func_name = line.split()[1].split('(')[0]
                if not re.match(r'^[a-z_][a-z0-9_]*$', func_name):  # Function names must be snake_case
                    incorrect_functions.append(func_name)

        return {
            "Incorrect Classes": incorrect_classes,
            "Incorrect Functions": incorrect_functions,
        }

    def docstrings(self):
        """Extract docstrings from classes and functions."""
        self.file.seek(0)
        doc_report = []
        for node in self._parse_ast():
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                docstring = ast.get_docstring(node)
                if docstring:
                    doc_report.append(f"{node.name}:\n{docstring}\n")
                else:
                    doc_report.append(f"{node.name}: DocString not found\n")
        return doc_report

    def type_annotation_check(self):
        """Check if all functions and methods use type annotations, including __init__."""
        missing_annotations = []
        for node in self._parse_ast():
            if isinstance(node, ast.FunctionDef):
                # Check if the function/method has a return type annotation
                has_return_annotation = node.returns is not None

                # Check if all arguments (except 'self' in methods) have type annotations
                args_have_annotations = all(arg.annotation for arg in node.args.args if arg.arg != 'self')

                if not has_return_annotation or not args_have_annotations:
                    missing_annotations.append(node.name)

        if not missing_annotations:
            return "All functions and methods use type annotations."
        else:
            return f"Functions without type annotations: {', '.join(missing_annotations)}"

    def _parse_ast(self):
        """Parse the file as an AST."""
        self.file.seek(0)  # Reset file pointer
        return ast.walk(ast.parse(self.file.read()))


def main():
    filename = input("Please enter the Python file name (must include .py extension): ").strip()
    while not filename.endswith('.py'):
        print("Must include .py extension.")
        filename = input("Please enter the file name (must include .py extension): ").strip()

    report = f'style_report_{filename}.txt'

    print("We will now conduct a report on this Python file.")

    with open(filename, 'r') as check:
        new_check = File(check)
        tallies = new_check.file_structure()
        name_issues = new_check.name_convention()
        doc_report = new_check.docstrings()
        annotation_check = new_check.type_annotation_check()

    with open(report, 'w') as txt:
        txt.write("Python File Analysis Report\n")
        txt.write("===========================\n")
        txt.write("Here is the file structure:\n")
        txt.write(f"Total non-empty lines: {tallies['Lines']}\n")
        txt.write(f"Total packages imported: {tallies['Packages']}\n")
        txt.write(f"Total classes defined: {tallies['Classes']}\n")
        txt.write(f"Total top-level functions: {tallies['Functions']}\n\n")

        txt.write("Here are the Doc Strings:\n")
        txt.write("===========================\n")
        for doc in doc_report:
            txt.write(doc + '\n')

        txt.write("Naming Convention Issues:\n")
        txt.write("===========================\n")
        if name_issues["Incorrect Classes"]:
            txt.write("Incorrect Class Names:\n")
            for cls in name_issues["Incorrect Classes"]:
                txt.write(f"- {cls}\n")
        else:
            txt.write("All class names follow the CamelCase convention.\n")

        if name_issues["Incorrect Functions"]:
            txt.write("Incorrect Function Names:\n")
            for fn in name_issues["Incorrect Functions"]:
                txt.write(f"- {fn}\n")
        else:
            txt.write("All function names follow the snake_case convention.\n")

        txt.write("Type Annotation Check:\n")
        txt.write("===========================\n")
        txt.write(annotation_check + '\n')


if __name__ == "__main__":
    main()