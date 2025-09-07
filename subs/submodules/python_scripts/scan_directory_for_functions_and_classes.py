# -*- coding: utf-8 -*-
import os
import ast
import csv
import xlsxwriter

def analyze_file(file_path, project_root_directory):
    """
    Analyze a Python file and return a list of classes and functions defined in it.

    :param file_path: Path to the .py file to be analyzed.
    :type file_path: str
    :param project_root_directory: The root directory to make paths relative.
    :type project_root_directory: str
    :return: List of tuples containing file name, type (class/function), name, and line.
    :rtype: list
    """
    results = []
    relative_file_path = os.path.relpath(file_path, project_root_directory)  # Convert to relative path
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError as e:
        print(f"Syntax error while analyzing the file {relative_file_path}: {e}")
        return results

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):  # Classes
            results.append((relative_file_path, 'class', node.name, node.lineno))
        elif isinstance(node, ast.FunctionDef):  # Functions or methods
            results.append((relative_file_path, 'function', node.name, node.lineno))

    return results


def scan_directory_for_functions_and_classes(directory):
    """
    Scan all .py files in the directory and return a list of found classes and functions.

    :param directory: Directory to be scanned.
    :type directory: str
    :return: List of tuples containing file path, type (class/function), name, and line.
    :rtype: list
    """
    all_results = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_results = analyze_file(file_path, directory)
                all_results.extend(file_results)

    return all_results


def save_to_csv(data, output_file):
    """
    Save the results to a CSV file.

    :param data: List of data to be saved.
    :type data: list
    :param output_file: Path to the output CSV file.
    :type output_file: str
    """
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['File', 'Type', 'Name', 'Line'])  # Headers
        writer.writerows(data)
    print(f"Data saved in {output_file}")

def save_to_xlsx(data, output_file):
    """
    Save the results to an XLSX file.

    :param data: List of data to be saved.
    :type data: list
    :param output_file: Path to the output XLSX file.
    :type output_file: str
    """
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()

    # Write headers
    worksheet.write(0, 0, 'File')
    worksheet.write(0, 1, 'Type')
    worksheet.write(0, 2, 'Name')
    worksheet.write(0, 3, 'Line')

    # Write data
    for row_num, row_data in enumerate(data, start=1):
        worksheet.write(row_num, 0, row_data[0])
        worksheet.write(row_num, 1, row_data[1])
        worksheet.write(row_num, 2, row_data[2])
        worksheet.write(row_num, 3, row_data[3])

    workbook.close()
    print(f"Data saved in {output_file}")


# Project root directory (where the script is executed)
project_root_directory = os.path.dirname(os.path.abspath(__file__))

# Scan the directory to find all classes, methods, and functions
results = scan_directory_for_functions_and_classes(project_root_directory)

# Ask the user if they want to save as CSV or XLSX
output_choice = input("Do you want to save the mapping as CSV or XLSX? (csv/xlsx): ").strip().lower()

if output_choice == 'csv':
    save_to_csv(results, 'files_classes_functions_mapping.csv')
elif output_choice == 'xlsx':
    save_to_xlsx(results, 'files_classes_functions_mapping.xlsx')
else:
    print("Invalid option. Exiting without saving.")

# References

# [1] OPENAI.
# Mapping of classes, functions, and methods.
# Available at: <https://chatgpt.com/c/analysis-python-code>.
# Accessed on: 08/09/2024.
