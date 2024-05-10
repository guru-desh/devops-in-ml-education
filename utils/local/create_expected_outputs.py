import os
import subprocess

from rich.console import Console

console = Console()


def build_conda_docker():
    console.print("Building Conda Docker image...", style="green")
    subprocess.run(
        [
            "docker",
            "build",
            "--platform=linux/amd64",
            "--build-arg",
            f"USER_ID={os.getuid()}",
            "--build-arg",
            f"GROUP_ID={os.getgid()}",
            "-t",
            "hw-runner",
            "-f",
            "src/utils/build-conda/Dockerfile",
            ".",
        ],
        check=True,
    )


def clean_docker():
    console.print("Cleaning up Docker environment...", style="green")
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}:/app",
            "hw-runner",
            "poetry",
            "run",
            "poe",
            "clean",
        ],
        check=True,
    )


def execute_notebook():
    console.print("Executing Jupyter Notebook...", style="green")
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}:/app",
            "hw-runner",
            "poetry",
            "run",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--inplace",
            "src/teacher_files/HW2_Solutions.ipynb",
            "--debug",
        ],
        check=True,
    )


def remove_solutions():
    console.print("Removing solutions from Notebook...", style="green")
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}:/app",
            "hw-runner",
            "poetry",
            "run",
            "python3",
            "src/utils/remove_solution_code/remove_solution_code_from_notebook.py",
            "--input_path",
            "src/teacher_files/HW2_Solutions.ipynb",
            "--output_path",
            "src/teacher_files/HW2_Solutions_Removed.ipynb",
        ],
        check=True,
    )


def convert_to_html():
    console.print("Converting Notebook to HTML...", style="green")
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}:/app",
            "hw-runner",
            "poetry",
            "run",
            "jupyter",
            "nbconvert",
            "--to",
            "html",
            "src/teacher_files/HW2_Solutions_Removed.ipynb",
        ],
        check=True,
    )


def convert_to_pdf():
    console.print("Converting HTML to PDF...", style="green")
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}:/app",
            "hw-runner",
            "poetry",
            "run",
            "python3",
            "src/utils/expected_outputs/convert_to_pdf.py",
            "--html_file",
            "src/teacher_files/HW2_Solutions_Removed.html",
            "--pdf_file",
            "src/teacher_files/HW2_Solutions_Removed.pdf",
        ],
        check=True,
    )


def watermark_pdf():
    console.print("Adding watermark to PDF...", style="green")
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}:/app",
            "hw-runner",
            "poetry",
            "run",
            "watermark",
            "grid",
            "-h",
            "5",
            "-v",
            "5",
            "-o",
            "0.3",
            "-a",
            "45",
            "--text-size",
            "24",
            "--save",
            "src/teacher_files/HW2_Expected_Output.pdf",
            "src/teacher_files/HW2_Solutions_Removed.pdf",
            "EXPECTED-OUTPUT",
        ],
        check=True,
    )


def clean_intermediate_files():
    console.print("Cleaning intermediate files...", style="green")
    os.remove("src/teacher_files/HW2_Solutions_Removed.ipynb")
    os.remove("src/teacher_files/HW2_Solutions_Removed.html")
    os.remove("src/teacher_files/HW2_Solutions_Removed.pdf")


def create_expected_outputs():
    build_conda_docker()
    execute_notebook()
    remove_solutions()
    convert_to_html()
    convert_to_pdf()
    watermark_pdf()
    clean_docker()
    clean_intermediate_files()


if __name__ == "__main__":
    create_expected_outputs()
