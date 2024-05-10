import argparse
import json
import os
import sys

from rich.console import Console

console = Console()


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Parse test results from a JSON file")
    parser.add_argument(
        "--input_path", help="Path to the JSON file containing test results"
    )
    args = parser.parse_args()

    # Convert input path to absolute path
    args.input_path = os.path.abspath(args.input_path)

    # Read and parse the JSON file
    with open(args.input_path, "r") as file:
        data = json.load(file)

    # Initialize variables for tracking test results
    total_score = 0
    any_test_failed = False

    # Iterate through the tests
    for test in data["tests"]:
        if "max_score" not in test:
            raise ValueError(
                "Test missing 'max_score' field. This is indicative of an issue with the autograder."
            )
        total_score += test["max_score"]
        if test["status"] != "passed":
            any_test_failed = True

    # Calculate and print the results
    result_score = f"{data['score']}/{total_score}"
    console.print(f"Autograder score: {result_score}", style="bold")

    # Exit with code 1 if any test failed
    if any_test_failed:
        console.print("One or more tests failed.", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main()
