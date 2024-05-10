# From: https://github.gatech.edu/Machine-Learning/automation/blob/main/build_autograder/build_autograder.py

import glob
import json
import os
import sys
from datetime import datetime
from zipfile import ZipFile


def build_run_autograder_file():
    """
    Returns the string contents of the run_autograder file, which varies
    per autograder by copying student submission files to a source directory
    """
    res = """#!/usr/bin/env bash
# Set up autograder files
"""

    # Copy student submission directory into source directory and rename as student_files
    res += "cp -r /autograder/submission /autograder/source/\n"
    res += "mv /autograder/source/submission /autograder/source/student_files\n"

    res += """cd /autograder/source
export PYTHONDONTWRITEBYTECODE=1
python3 run_tests.py > /autograder/results/results.json
"""
    return res


def build_setup_file():
    """
    Returns the string contents of setup.sh, which installs initial dependencies
    for the Docker container. Doesn't change between autograders.
    """
    return """#!/usr/bin/env bash
apt-get install zlib1g
apt-get install -y python3-dev python3-pip 
pip3 install -r /autograder/source/autograder/requirements.txt
"""


def copy_directory(zip_file, directory):
    """
    Copies an entire directory to the root of the given ZIP file object
    """
    for dirpath, dirs, files in os.walk(directory):
        for f in files:
            fn = os.path.join(dirpath, f)
            zip_file.write(fn)


def verify_required_files():
    """
    Verifies that all required files for the autograder exist
    """
    required_files = [
        "autograder/config.json",
        "autograder/requirements.txt",
        "autograder/autograder_utils.py",
        "autograder/tests",
        "run_tests.py",
        "teacher_files",
    ]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Could not find {file} in root of {os.getcwd()}.")
            print("Be sure that the current working directory is HW/src.")
            return False
    return True


def createZIP():
    """
    Creates all the autograders per the config specified in config.json.

    Repackage files into a zip file that will be unpacked when uploaded to gradescope.
    The structure must match gradescope's expectations.
    """
    # Check if required files exist
    if not verify_required_files():
        return

    # Open config json
    f = open("autograder/config.json")
    config = json.load(f)
    f.close()

    failures = 0

    now = datetime.now()
    date_str = now.strftime("%b-%d-%H%M")

    for name, properties in config.items():
        zip_name = f"autograder/{name}.zip"
        try:
            with ZipFile(zip_name, "w") as zip_file:
                # Write all boilerplate files
                zip_file.write(
                    "autograder/requirements.txt", "autograder/requirements.txt"
                )
                zip_file.write(
                    "autograder/autograder_utils.py", "autograder/autograder_utils.py"
                )
                zip_file.write("run_tests.py", "run_tests.py")
                zip_file.writestr("run_autograder", build_run_autograder_file())
                zip_file.writestr("setup.sh", build_setup_file())

                # Write the tests files to the autograder directory
                for test_name in properties["tests"]:
                    test_path = f"autograder/tests/{test_name}"
                    zip_file.write(test_path, test_path)

                # Write the solutions files to teacher_files directory
                for file in properties["solutions"]:
                    zip_file.write(f"teacher_files/{file}", f"teacher_files/{file}")

                # all_teacher_files = glob.glob("teacher_files/**/*.py", recursive=True)
                # for file in all_teacher_files:
                #     zip_file.write(file, file)

                # Copy necessary data folders to teacher_files directory
                for folder in properties["copy-dir"]:
                    for file in glob.glob(f"autograder/{folder}/**/*", recursive=True):
                        zip_file.write(
                            file, f"autograder/{folder}/{os.path.basename(file)}"
                        )

                # Copy all files from the teacher_files/mark_student_functions directory into teacher_files/mark_student_functions
                for file in glob.glob("teacher_files/mark_student_functions/*"):
                    zip_file.write(file, file)

            print(f"Created autograder for {name}")

        except Exception as e:
            failures += 1
            print(f"ERROR: Failed to make autograder for {name}:")

            # Print the stack trace
            print(e)

            # Delete zip file if it exists
            if os.path.exists(zip_name):
                os.remove(zip_name)

            sys.exit(1)

    if not failures:
        print("\nAll autograders generated!\n")

    print(f"All outputs are located in src/autograder")


if __name__ == "__main__":
    # This script must be run within the src directory.
    print("\nBuilding autograder zip.\n")

    createZIP()

    print("\nComplete.\n")
