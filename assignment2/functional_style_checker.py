import re
import ast


def count_lines(file_content):
    """Count non-empty lines in the file content."""
    return sum(1 for line in file_content.splitlines() if line.strip())


def parse_ast(file_content):
    """Parse the file content into an AST tree."""
    return ast.parse(file_content)


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


def check_name_conventions(file_content):
    """Check if class and function names follow naming conventions."""
    incorrect_classes = []
    incorrect_functions = []

    for line in file_content.splitlines():
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
    """Check if all functions and methods use type annotations."""
    def is_fully_annotated(node):
        if node.name == "__init__":
            return all(arg.annotation for arg in node.args.args if arg.arg != "self")
        return node.returns is not None and all(arg.annotation for arg in node.args.args if arg.arg != "self")

    missing_annotations = [
        node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and not is_fully_annotated(node)
    ]

    return "All functions and methods use type annotations." if not missing_annotations else \
        f"Functions without type annotations: {', '.join(missing_annotations)}"


def analyze_file(file_content):
    """Perform analysis on the given file content."""
    tree = parse_ast(file_content)
    total_lines = count_lines(file_content)
    imports = extract_imports(tree)
    classes, functions = extract_classes_and_functions(tree)
    incorrect_classes, incorrect_functions = check_name_conventions(file_content)
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
    report_lines = [
        "Python File Analysis Report",
        "===========================",
        f"Total non-empty lines: {report['Total Lines']}",
        f"Packages imported: {', '.join(report['Imports']) if report['Imports'] else 'None'}",
        f"Classes defined: {', '.join(report['Classes']) if report['Classes'] else 'None'}",
        f"Top-level functions: {', '.join(report['Functions']) if report['Functions'] else 'None'}",
        "",
        "Docstrings:",
        "==========================="
    ]
    report_lines.extend(report['Docstrings'])
    report_lines.append("Naming Convention Issues:")
    report_lines.append("===========================")

    if report['Incorrect Classes']:
        report_lines.append("Incorrect Class Names:")
        report_lines.extend(f"- {cls}" for cls in report['Incorrect Classes'])
    else:
        report_lines.append("All class names follow the CamelCase convention.")

    if report['Incorrect Functions']:
        report_lines.append("Incorrect Function Names:")
        report_lines.extend(f"- {fn}" for fn in report['Incorrect Functions'])
    else:
        report_lines.append("All function names follow the snake_case convention.")

    report_lines.append("Type Annotation Check:")
    report_lines.append("===========================")
    report_lines.append(report['Type Annotations'])

    with open(f"style_report_{filename}.txt", 'w') as txt:
        txt.write('\n'.join(report_lines))


def main():
    filename = input("Please enter the Python file name (must include .py extension): ").strip()
    while not filename.endswith('.py'):
        print("Must include .py extension.")
        filename = input("Please enter the file name (must include .py extension): ").strip()

    print("We will now conduct a report on this Python file.")

    with open(filename, 'r') as file:
        file_content = file.read()

    report = analyze_file(file_content)
    write_report(filename, report)


if __name__ == "__main__":
    main()
