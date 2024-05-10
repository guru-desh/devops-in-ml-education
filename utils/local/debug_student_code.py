import argparse
import json
import os
import subprocess
import sys

from rich.console import Console

console = Console()

# Define the path to the autograder config file
PATH_TO_CONFIG = "src/autograder/config.json"


def load_in_autograder_config():
    """Loads in the autograder config file"""
    with open(PATH_TO_CONFIG, "r") as config_file:
        autograders = json.load(config_file)

    return autograders


# Define the command-line arguments
parser = argparse.ArgumentParser(
    description="Debug student code using local autograder"
)
parser.add_argument(
    "--autograder",
    help="Name of the autograder to use",
    type=str,
    required=True,
)
parser.add_argument(
    "--student_code_path",
    help="Path to the student code",
    type=str,
    required=True,
)
parser.add_argument(
    "--rebuild",
    help="Rebuild the autograder Docker image",
    action="store_true",
)


def run_command(command, cwd=None):
    """Run a command and handle exceptions, including printing the error output."""
    try:
        # Using `subprocess.run` to capture output for more detailed error reporting
        _ = subprocess.run(command, check=True, text=True, cwd=cwd)

    except subprocess.CalledProcessError as e:
        print(
            f"Command '{' '.join(e.cmd)}' returned non-zero exit status {e.returncode}.",
            file=sys.stderr,
        )
        print(f"Error output:\n{e.stderr}", file=sys.stderr)
        sys.exit(e.returncode)


def check_if_autograder_docker_exists(autograder):
    """Check if the Docker image for the autograder exists"""
    autograder_exists = False
    try:
        _ = subprocess.run(
            ["docker", "inspect", f"hw-autograder-{autograder.lower()}"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        autograder_exists = True
    except subprocess.CalledProcessError:
        pass

    return autograder_exists


def build_autograder_docker_image(autograder):
    """Build the Docker image for the autograder"""
    console.print(
        f"Building Docker image for autograder {autograder}...", style="green"
    )
    run_command(
        [
            "docker",
            "build",
            "--build-arg",
            f"ZIP_FILE=src/autograder/{autograder}.zip",
            "-t",
            f"hw-autograder-{autograder.lower()}",
            "-f",
            "src/utils/autograder/Dockerfile",
            ".",
        ]
    )


def run_autograder(autograder, student_code_path):
    """Run the autograder"""
    # Make results directory if it doesn't exist
    if not os.path.exists("autograder_results"):
        os.makedirs("autograder_results")

    # Run Docker container
    console.print(f"Running autograder {autograder}...", style="green")
    run_command(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{student_code_path}:/autograder/submission",
            "-v",
            f"{os.getcwd()}/autograder_results:/autograder/results",
            f"hw-autograder-{autograder.lower()}:latest",
            "/autograder/run_autograder",
        ]
    )


def parse_autograder_results():
    """Parse the autograder results"""
    console.print("Parsing JSON output...", style="green")
    run_command(
        [
            "poetry",
            "run",
            "python3",
            "src/utils/autograder/parse_json_output.py",
            "--input_path",
            "autograder_results/results.json",
        ],
    )


def main():
    """
    Example usage:
    poetry run poe debug_student_code --autograder <autograder_name> --student_code_path <path_to_student_code> --rebuild
    """

    """
    Pseudo code:
    1. Check if the autograder Docker image exists or if the user wants to rebuild it
    2. If it doesn't exist, build the autograder Docker image
    3. Run the student code in the autograder Docker image
    4. Print the results
    5. Parse autograder results
    """

    args = parser.parse_args()
    selected_autograder = args.autograder
    student_code_path = args.student_code_path
    rebuild = args.rebuild

    available_autograders = load_in_autograder_config()

    if selected_autograder not in available_autograders:
        raise ValueError(
            f"""
        Autograder {selected_autograder} not found in available autograders: {available_autograders}
        """
        )

    if not check_if_autograder_docker_exists(selected_autograder) or rebuild:
        # Change directory and build autograder
        build_autograder_docker_image(selected_autograder)

    # Make results directory if it doesn't exist
    if not os.path.exists("autograder_results"):
        os.makedirs("autograder_results")

    # Make sure the student code path is absolute
    student_code_path = os.path.abspath(student_code_path)

    # Run Docker container
    run_autograder(selected_autograder, student_code_path)

    # Display results
    console.print("Results:", style="green")
    with open("autograder_results/results.json", "r") as results_file:
        print(results_file.read())

    # Run parse_json_output.py
    parse_autograder_results()


if __name__ == "__main__":
    main()
