import argparse

# Run the command to see all the libraries on python
import nbformat
from nbformat import NotebookNode


def remove_solution_cells(notebook: NotebookNode) -> NotebookNode:
    """
    Remove cells that contain 'SOLUTION'. Keep code cells with outputs but remove their source.
    """
    new_cells = []
    for cell in notebook.cells:
        if "SOLUTION" in cell.source:
            if cell.cell_type == "code" and cell.outputs:
                # Keep the outputs, remove the source
                cell.source = ""
                new_cells.append(cell)
            # Completely remove markdown cells and code cells without outputs
            if cell.cell_type == "markdown":
                cell.source = ""
                new_cells.append(cell)
        else:
            new_cells.append(cell)

    notebook.cells = new_cells
    return notebook


def remove_outputs(notebook: NotebookNode) -> NotebookNode:
    """
    Remove outputs from cells with '# REMOVE OUTPUT #' and clean the marker.
    """
    for cell in notebook.cells:
        if cell.cell_type == "code" and "# REMOVE OUTPUT #" in cell.source:
            cell.outputs = []
            cell.source = cell.source.replace("# REMOVE OUTPUT #", "")

    return notebook


def process_notebook(input_path: str, output_path: str):
    """
    Load, process, and save the notebook.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    notebook = remove_solution_cells(notebook)
    notebook = remove_outputs(notebook)

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
