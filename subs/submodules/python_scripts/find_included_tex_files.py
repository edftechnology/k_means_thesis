# -*- coding: utf-8 -*-
"""
Script to identify all files referenced in a LaTeX project (.tex, images, code listings, etc.).
It lists:
- All .tex files that were checked
- Files referenced but not found
- Files that exist but are not used (can be deleted)

Usage:
    python find_included_tex_files.py <main.tex>

It will ask for confirmation before deleting unused files.
"""

import os
import re
import fnmatch

def find_included_files(tex_file, checked_files=None, missing_files=None):
    """
    Verifica os arquivos referenciados no projeto LaTeX, incluindo arquivos .tex filhos,
    e retorna uma lista de arquivos utilizados, ignorando linhas comentadas.
    """
    if checked_files is None:
        checked_files = set()
    if missing_files is None:
        missing_files = set()

    included_files = set()
    patterns = [
        r'\\includegraphics(?:\[[^\]]*\])?{([^}]+)}',  # Imagens
        r'\\bibliography{([^}]+)}',                   # Bibliografia
        r'\\include{([^}]+)}',                        # Arquivos .tex incluídos
        r'\\input{([^}]+)}',                          # Arquivos .tex incluídos
        r'\\usepackage{([^}]+)}',                     # Pacotes locais (.sty)
        r'\\lstinputlisting(?:\[[^\]]*\])?{([^}]+)}'  # Código fonte (.py, .cpp etc.)
    ]
    
    if tex_file.lower() in checked_files:
        return included_files, missing_files

    checked_files.add(tex_file.lower())

    try:
        with open(tex_file, 'r', encoding='utf-8') as file:
            print(f"🔎 Processing file: {tex_file}")
            for line in file:
                line = line.strip()
                if line.startswith('%'):
                    continue
                
                for pattern in patterns:
                    matches = re.findall(pattern, line, flags=re.IGNORECASE)
                    for match in matches:
                        if pattern.startswith(r'\\(include|input)'):
                            match += '.tex' if not match.endswith('.tex') else ''
                        included_files.add(os.path.normpath(match.lower()))

                        if match.endswith('.tex'):
                            sub_included, sub_missing = find_included_files(
                                match, checked_files, missing_files
                            )
                            included_files.update(sub_included)
                            missing_files.update(sub_missing)
    except FileNotFoundError:
        print(f"❌ File not found: {tex_file}")
        missing_files.add(tex_file)

    return included_files, missing_files

def find_all_files(directory, excluded_files_and_dirs=None):
    """
    Retorna uma lista de todos os arquivos no diretório e subdiretórios,
    exceto os que estão na lista de exclusão.
    """
    if excluded_files_and_dirs is None:
        excluded_files_and_dirs = []

    all_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(
            os.path.relpath(os.path.join(root, d), directory).lower(), excl.lower())
            for excl in excluded_files_and_dirs)]

        for file in files:
            filepath = os.path.relpath(os.path.join(root, file), directory).lower()
            if any(fnmatch.fnmatch(filepath, excl.lower()) for excl in excluded_files_and_dirs):
                continue
            all_files.append(filepath)
    return set(all_files)

def find_all_tex_files(directory):
    """
    Encontra todos os arquivos .tex no diretório especificado.
    """
    tex_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".tex"):
                tex_files.append(os.path.relpath(os.path.join(root, file), directory).lower())
    return tex_files

def confirm_deletion():
    """
    Pergunta ao usuário se deseja excluir os arquivos não utilizados.
    """
    while True:
        response = input("\nDo you want to delete the unused files? (y/n): ").lower()
        if response == 'y':
            confirm = input("Are you sure? This action cannot be undone! (y/n): ").lower()
            if confirm == 'y':
                return True
            else:
                print("⚠️  Deletion canceled.")
                return False
        elif response == 'n':
            return False
        else:
            print("Invalid input. Please type 'y' or 'n'.")

def remove_dirs_with_only_unused_files(root_dir, unused_files):
    """
    Remove diretórios que contêm apenas arquivos não utilizados.
    """
    print("\n🧹 Removing directories that contain only unused files...")

    unused_abs_paths = {os.path.abspath(f) for f in unused_files}

    for dirpath, _, filenames in os.walk(root_dir, topdown=False):
        if any(part.startswith('.') or part == '__pycache__' for part in dirpath.split(os.sep)):
            continue

        abs_files_in_dir = {os.path.abspath(os.path.join(dirpath, f)) for f in filenames}
        
        if abs_files_in_dir and abs_files_in_dir.issubset(unused_abs_paths):
            try:
                for f in abs_files_in_dir:
                    if os.path.isfile(f):
                        print(f"🗑️  Deleting unused file: {f}")
                        os.remove(f)
                if not os.listdir(dirpath):
                    os.rmdir(dirpath)
                    print(f"📁 Deleted directory: {dirpath}")
            except (OSError, PermissionError) as e:
                print(f"⚠️  Could not remove '{dirpath}': {e}")

def remove_empty_dirs(directory):
    """
    Remove recursivamente diretórios vazios, ignorando qualquer diretório .git.
    """
    for root, dirs, _ in os.walk(directory, topdown=False):
        for d in dirs:
            dirpath = os.path.join(root, d)
            if ".git" in dirpath:
                continue
            try:
                if not os.listdir(dirpath):
                    os.rmdir(dirpath)
                    print(f"🧺 Deleted empty directory: {dirpath}")
            except (OSError, PermissionError) as e:
                print(f"⚠️  Could not delete '{dirpath}': {e}")

def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python find_included_tex_files.py <main.tex>")
        return

    main_tex_file = sys.argv[1]
    project_dir = '.'

    print("🔍 Searching for all .tex files in the project...")
    all_tex_files = find_all_tex_files(project_dir)

    all_included_files = set()
    missing_files = set()
    checked_files = set()

    included_files, file_missing = find_included_files(main_tex_file, checked_files, missing_files)
    all_included_files.update(included_files)
    missing_files.update(file_missing)
    all_included_files.add(main_tex_file.lower())

    print("🔍 Searching for all files in the project directory...")
    all_files = find_all_files(project_dir, excluded_files_and_dirs=[
        '.git',
        '__pycache__',
        '*.aux',
        '*.log',
        '*.out',
        '*.pdf',
        '*.toc',
        '*.fls',
        '*.fdb_latexmk',
        '*.gz',
        '*.bbl',
        '*.lof',
        '*.lot',
        '*.synctex.gz',
        '*.nav',
        '*.snm',
        '*.vrb',
        '*.bak',
        '*.pyc',
        os.path.basename(__file__).lower()
    ])

    base_files = {os.path.splitext(file)[0] for file in all_included_files}
    unused_files = {file for file in all_files if os.path.splitext(file)[0] not in base_files}

    print("\n📄 Checked .tex files:")
    for file in sorted(checked_files):
        print(f" - file://{os.path.abspath(file)}")
    if len(checked_files) == 0:
        print(" - No .tex files were checked.")

    print("\n❌ Referenced but missing files:")
    for file in sorted(missing_files):
        print(f" - {file}")
    if len(missing_files) == 0:
        print(" - No missing files found.")

    print("\n🗂️  Unused files (candidates for deletion):")
    for file in sorted(unused_files):
        print(f" - file://{os.path.abspath(file)}")
    if len(unused_files) == 0:
        print(" - No unused files found.")

    if unused_files:
        if confirm_deletion():
            for file in unused_files:
                if os.path.exists(file):
                    print(f"🧽 Deleting file: {file}")
                    os.remove(file)

            remove_dirs_with_only_unused_files(project_dir, unused_files)
            remove_empty_dirs(project_dir)
            print("✅ Cleanup complete.")

if __name__ == "__main__":
    main()

# References

# [1] OPENAI.
# Finding included files.
# Available at: <https://chatgpt.com/c/26f31d3e-47f0-4933-bee8-3188c5c20aaf>
# Accessed on: 08/17/2024.
