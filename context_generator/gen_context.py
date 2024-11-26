#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
from pathlib import Path
import fnmatch


def usage():
    print(f"Usage: {sys.argv[0]} [directory]")
    print("Concatenates selected files from the specified directory (default: current directory).")
    sys.exit(1)


def copy_to_clipboard(text):
    try:
        subprocess.run('pbcopy', text=True, input=text, check=True)
        print("Output copied to clipboard using pbcopy.")
    except subprocess.CalledProcessError:
        print("Failed to copy to clipboard. Please ensure 'pbcopy' is available.")


def should_ignore(path, ignore_patterns):
    """
    Check if the given path matches any of the ignore patterns.
    """
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path.name, pattern):
            return True
    return False


def collect_files(directory, ignore_patterns):
    """
    Traverse the directory and collect files that do not match the ignore patterns.
    """
    collected_files = []
    for root, dirs, files in os.walk(directory):
        # Convert root to Path object
        root_path = Path(root)

        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(Path(d), ignore_patterns)]

        for file in files:
            file_path = root_path / file
            if not should_ignore(file_path, ignore_patterns):
                collected_files.append(file_path)

    return collected_files


def main():
    parser = argparse.ArgumentParser(description="Concatenate selected files with proper formatting.")
    parser.add_argument('directory', nargs='?', default='.', help='Directory to search files in')
    args = parser.parse_args()

    directory = Path(args.directory).resolve()

    if not directory.is_dir():
        print(f"The specified path '{directory}' is not a directory.")
        sys.exit(1)

    # Define ignore patterns (similar to tree's -I option)
    ignored_patterns = [
        'node_modules', '.next', '.ignore', '.DS_Store',
        '*.app', 'out', '.git', 'dist', 'build',
        '*.pyc', '__pycache__', '.pytest_cache', '.idea'
    ]

    # Collect files excluding ignored patterns
    files = collect_files(directory, ignored_patterns)

    if not files:
        print("No files found in the specified directory.")
        sys.exit(1)

    # Generate a list of relative file paths for fzf
    relative_files = [f.relative_to(directory) for f in files]
    file_list = '\n'.join(str(f) for f in relative_files)

    # Use fzf for interactive selection
    try:
        fzf = subprocess.Popen(
            ['fzf', '-m', '--prompt=Select files to concatenate: '],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )
        selected_rel = fzf.communicate(input=file_list)[0].strip().split('\n')
    except Exception as e:
        print(f"Error during file selection: {e}")
        sys.exit(1)

    if not selected_rel or selected_rel == ['']:
        print("No files selected. Exiting.")
        sys.exit(0)

    # Convert selected relative paths back to absolute paths
    selected = [directory / Path(rel) for rel in selected_rel]

    output = ""

    for file in selected:
        fname = file.name
        ext = file.suffix[1:] if file.suffix else 'txt'

        if not os.access(file, os.R_OK):
            print(f"Warning: Cannot read file '{file}'. Skipping.")
            continue

        try:
            with file.open('r', encoding='utf-8') as f:
                content = f.read().replace('`', '\\`')
        except Exception as e:
            print(f"Warning: Error reading file '{file}': {e}. Skipping.")
            continue

        if not content:
            print(f"Warning: File '{file}' is empty.")

        output += f"### {fname}\n```{ext}\n{content}\n```\n\n"

    if not output:
        print("No content to display or copy.")
        sys.exit(0)

    # Append directory tree if 'tree' is available
    if subprocess.run(['which', 'tree'], stdout=subprocess.PIPE).returncode == 0:
        tree_output = subprocess.run([
            'tree', '-L', '10',
            '-I', '|'.join(ignored_patterns),
            '.'
        ], cwd=directory, stdout=subprocess.PIPE, text=True).stdout
        output += f"### Directory Tree\n```bash\n{tree_output}\n```\n"
    else:
        output += "### Directory Tree\nInstall 'tree' for directory visualization: brew install tree (macOS)\n"

    copy_to_clipboard(output)


if __name__ == "__main__":
    main()
