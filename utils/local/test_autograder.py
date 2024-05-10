import json
import os
import subprocess
import sys

from rich.console import Console

console = Console()

PATH_TO_CONFIG = "src/autograder/config.json"


def load_in_autograder_config():
    """Loads in the autograder config file"""
    with open(PATH_TO_CONFIG, "r") as config_file:
        config = json.load(config_file)

    autograders = list(config.keys()) + ["All"]
    return autograders


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


def main(autograder):
    # Change directory and build autograder
    console.print(f"Building autograder {autograder}...", style="green")
    run_command(["python3", "utils/autograder/build_autograder.py", "./"], cwd="src")

    # Build Docker image
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
            f"{os.getcwd()}/src/teacher_files:/autograder/submission",
            "-v",
            f"{os.getcwd()}/autograder_results:/autograder/results",
            f"hw-autograder-{autograder.lower()}:latest",
            "/autograder/run_autograder",
        ]
    )

    # Display results
    console.print("Results:", style="green")
    with open("autograder_results/results.json", "r") as results_file:
        print(results_file.read())

    # Run parse_json_output.py
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


if __name__ == "__main__":
    autograder_options = load_in_autograder_config()

    if len(sys.argv) < 2:
        raise ValueError(
            f"""
            Usage: python build_and_run_autograder.py <autograder_name>"
            Available autograders: {autograder_options}
            """
        )

    autograder = sys.argv[1]
    if autograder not in autograder_options:
        raise ValueError(
            f"""
            Autograder {autograder} not found.
            Available autograders: {autograder_options}
            """
        )

    if autograder == "All":
        autograder_options.remove("All")
        for autograder in autograder_options:
            main(autograder)
    else:
        main(autograder)
