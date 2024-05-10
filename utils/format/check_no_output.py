import argparse

import nbformat


def check_notebook_outputs(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "code":
            if cell.outputs:
                return 1  # Return 1 if outputs are found
    return 0  # Return 0 if no outputs are found


def main():
    parser = argparse.ArgumentParser(
        description="Check a Jupyter Notebook for output cells."
    )
    parser.add_argument(
        "--notebook", help="Path to the Jupyter Notebook file", required=True
    )
    args = parser.parse_args()

    exit_code = check_notebook_outputs(args.notebook)
    exit(exit_code)


if __name__ == "__main__":
    main()
