import argparse

import nbformat
from nbformat import NotebookNode


def remove_empty_cells(notebook: NotebookNode) -> NotebookNode:
    """
    Remove all cells that are empty.
    """
    new_cells = [cell for cell in notebook.cells if cell.source.strip()]
    notebook.cells = new_cells
    return notebook


def process_notebook(input_path: str, output_path: str):
    """
    Load, process, and save the notebook.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    notebook = remove_empty_cells(notebook)

    with open(output_path, "w", encoding="utf-8") as f:
        nbformat.write(notebook, f)


def main():
    parser = argparse.ArgumentParser(description="Process Jupyter notebooks.")
    parser.add_argument(
        "--input_path", type=str, help="Path to the input Jupyter Notebook"
    )
    parser.add_argument(
        "--output_path", type=str, help="Path to the output Jupyter Notebook"
    )

    args = parser.parse_args()
    process_notebook(args.input_path, args.output_path)


if __name__ == "__main__":
    main()
