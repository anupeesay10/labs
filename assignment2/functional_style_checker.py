import re
import ast


def count_lines(file):
    """Count non-empty lines in the file."""
    file.seek(0)
    return sum(1 for line in file if line.strip())


def parse_ast(file):
    """Parse the file content into an AST tree."""
    file.seek(0)
    return ast.parse(file.read())


def extract_imports(tree):
    """Extract imported packages from the AST tree."""
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.append(', '.join(alias.name for alias in node.names))
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            imports.append(f"{module}: {', '.join(alias.name for alias in node.names)}")
    return imports


def extract_classes_and_functions(tree):
    """Extract class and top-level function names from the AST tree."""
    classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    return classes, functions


def check_name_conventions(file):
    """Check if class and function names follow naming conventions."""
    file.seek(0)
    incorrect_classes = []
    incorrect_functions = []

    for line in file:
        line = line.strip()
        if line.startswith("class "):
            class_name = line.split()[1].split('(')[0].strip(':')
            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', class_name):
                incorrect_classes.append(class_name)
        elif line.startswith("def "):
            func_name = line.split()[1].split('(')[0]
            if not re.match(r'^[a-z_][a-z0-9_]*$', func_name):
                incorrect_functions.append(func_name)

    return incorrect_classes, incorrect_functions



def extract_docstrings(tree):
    """Extract docstrings from classes and functions, including methods in classes."""
    docstrings = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_doc = ast.get_docstring(node)
            if class_doc:
                docstrings.append(f"Class {node.name}:\n{class_doc}\n")
            else:
                docstrings.append(f"Class {node.name}: DocString not found\n")

            # Check for docstrings in class methods
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_doc = ast.get_docstring(item)
                    if method_doc:
                        docstrings.append(f"Method {node.name}.{item.name}:\n{method_doc}\n")
                    else:
                        docstrings.append(f"Method {node.name}.{item.name}: DocString not found\n")

        elif isinstance(node, ast.FunctionDef):
            func_doc = ast.get_docstring(node)
            if func_doc:
                docstrings.append(f"Function {node.name}:\n{func_doc}\n")
            else:
                docstrings.append(f"Function {node.name}: DocString not found\n")

    return docstrings


def check_type_annotations(tree):
    """Check if all functions and methods use type annotations, including __init__."""
    missing_annotations = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check if the function is __init__
            if node.name == "__init__":
                # Ensure all arguments (excluding self) have annotations
                args_have_annotations = all(arg.annotation for arg in node.args.args if arg.arg != "self")
                if not args_have_annotations:
                    missing_annotations.append(node.name)
            else:
                # For other functions, check return type and argument annotations
                has_return_annotation = node.returns is not None
                args_have_annotations = all(arg.annotation for arg in node.args.args if arg.arg != "self")
                if not has_return_annotation or not args_have_annotations:
                    missing_annotations.append(node.name)

    if not missing_annotations:
        return "All functions and methods use type annotations."
    else:
        return f"Functions without type annotations: {', '.join(missing_annotations)}"


def analyze_file(file):
    """Perform analysis on the given file."""
    tree = parse_ast(file)
    total_lines = count_lines(file)
    imports = extract_imports(tree)
    classes, functions = extract_classes_and_functions(tree)
    incorrect_classes, incorrect_functions = check_name_conventions(file)
    docstrings = extract_docstrings(tree)
    type_annotation_report = check_type_annotations(tree)

    return {
        "Total Lines": total_lines,
        "Imports": imports,
        "Classes": classes,
        "Functions": functions,
        "Incorrect Classes": incorrect_classes,
        "Incorrect Functions": incorrect_functions,
        "Docstrings": docstrings,
        "Type Annotations": type_annotation_report,
    }


def write_report(filename, report):
    """Write the analysis report to a file."""
    with open(f"style_report_{filename}.txt", 'w') as txt:
        txt.write("Python File Analysis Report\n")
        txt.write("===========================\n")
        txt.write(f"Total non-empty lines: {report['Total Lines']}\n")
        txt.write(f"Packages imported: {', '.join(report['Imports']) if report['Imports'] else 'None'}\n")
        txt.write(f"Classes defined: {', '.join(report['Classes']) if report['Classes'] else 'None'}\n")
        txt.write(f"Top-level functions: {', '.join(report['Functions']) if report['Functions'] else 'None'}\n\n")

        txt.write("Docstrings:\n")
        txt.write("===========================\n")
        for doc in report['Docstrings']:
            txt.write(doc + '\n')

        txt.write("Naming Convention Issues:\n")
        txt.write("===========================\n")
        if report['Incorrect Classes']:
            txt.write("Incorrect Class Names:\n")
            for cls in report['Incorrect Classes']:
                txt.write(f"- {cls}\n")
        else:
            txt.write("All class names follow the CamelCase convention.\n")

        if report['Incorrect Functions']:
            txt.write("Incorrect Function Names:\n")
            for fn in report['Incorrect Functions']:
                txt.write(f"- {fn}\n")
        else:
            txt.write("All function names follow the snake_case convention.\n")

        txt.write("Type Annotation Check:\n")
        txt.write("===========================\n")
        txt.write(report['Type Annotations'] + '\n')


def main():
    filename = input("Please enter the Python file name (must include .py extension): ").strip()
    while not filename.endswith('.py'):
        print("Must include .py extension.")
        filename = input("Please enter the file name (must include .py extension): ").strip()

    print("We will now conduct a report on this Python file.")

    with open(filename, 'r') as file:
        report = analyze_file(file)

    write_report(filename, report)


if __name__ == "__main__":
    main()