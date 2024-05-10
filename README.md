# CI/CD pipeline

This README is very similar to the README that we provide to TAs. This has been anonymized as well. Not all files are provided (notably `src/teacher_files` or `src/autograder`) since they contain solutions to our assignments.

## Securing the Main branch

The main branch is locked and can only be edited via pull requests. There is at least one review required for the pull request along with a passing CI pipeline.

## Code quality checks and pre-commit

Code quality checks (mainly to format code and sort imports) have been added. These are all implemented using `poetry`.

### Make sure you do the following steps

1. Clone the repository
2. Create the conda environment via `conda env create -f src/environment/ml_hw2_env_[OS].yml` replacing `[OS]` with either `linux`, `mac`, or `win`.
3. Install `poetry` via either `pip install poetry` or `conda install -y poetry`
4. Run `poetry install --no-root` in the root of this repository. This will install all the dependencies to run code quality checks.
5. To run code quality checks, run `poetry run poe format`. This does the following:
2. Create the conda environment via `conda env create -f src/environment/ml_hw2_env_[OS].yml` replacing `[OS]` with either `linux`, `mac`, or `win`.
3. Install `poetry` via either `pip install poetry` or `conda install -y poetry`
4. Run `poetry install --no-root` in the root of this repository. This will install all the dependencies to run code quality checks.
5. To run code quality checks, run `poetry run poe format`. This does the following:
    - Runs `black` formatting on all python files and on the Jupyter Notebook
    - Sorts imports using `isort` on all python files and on the Jupyter Notebook
    - Clears all outputs from the Jupyter Notebook (this is helpful so during merge requests only differences in code are considered and not differences in output)
6. Run `pre-commit install` to install precommit, which will check formatting each time you commit your code. This saves you time since you don't have to wait until the automated build to see that you forgot to format your code!

The [automated builds](#automated-builds-and-test) will test formatting. This is done by running `poetry run poe check`.

## Development Tools

We provide some ways to easily test your results locally mainly via `poe`.

### Testing Autograder Locally

Running the autograder locally requires **Docker** to be installed. If you do not have Docker installed, please follow the instructions from the [official Docker website](https://docs.docker.com/engine/install/)

Use the `poetry run poe test_autograder` command to test autograders locally. An additional argument is needed to specify which autograder you want to test. The `poetry run poe test_autograder` will tell you which autograders are possible to test. For HW2, specifically, there are 5 options:

1. CS4641_HW2
2. CS7641_HW2
3. CS4641_HW2_Bonus_Undergrad
4. HW2_Bonus_All
5. All (which tests all of the above autograders at once)

For example, to test the CS4641_HW2 autograder, run `poetry run poe test_autograder CS4641_HW2`

### Running Formatting Checks Locally

In the CI/CD, the command to check for formatting is done via `poetry run poe check`. You can use this same command locally to see that your formatting is correct. Running `poetry run poe format` should resolve any errors that arise from the `poetry run poe check` command.

### Creating Expected Outputs Locally

Creating the expected outputs locally requires **Docker** to be installed. If you do not have Docker installed, please follow the instructions from the [official Docker website](https://docs.docker.com/engine/install/)

Running `poetry run poe create_expected_outputs` will create the expected outputs. **This only runs on Linux/Unix, so if you are on Windows, you need to use WSL.**

### Debugging Student Code using Local Autograder

Debugging Student Code using the local autograder locally requires **Docker** to be installed. If you do not have Docker installed, please follow the instructions from the [official Docker website](https://docs.docker.com/engine/install/).

Running `poetry run poe debug_student_code` will create the expected outputs. Here's the required arguments for this command:

1. **--autograder** specifies which autograder from [here](#testing-autograder-locally). Note that **All** is not a valid autograder to choose.
2. **--student_code_path** specifies the directory to where the student code is stored.

Here's the optional arguments for this command:

1. *--rebuild* rebuilds the docker container for the autograder even if already built.

An example command would be `poetry run poe debug_student_code --autograder CS4641_HW2 --student_code_path sample_student_submission`.

## Automated Builds and Test

One main change from Fall 2023's HW and this HW is the addition of a bunch of new automated tests and builds that didn't happen before. These automations speed up the creation of necessary files for the HW. Here's a couple of the things that these automations do:

- Autograder:
  1. Builds the autograder (replicates the exact steps that Gradescope does to create autograder)
  2. Tests solution files on the autograder
  3. Creates autograder `.zip` to be uploaded to Gradescope.

- Student Files:
  1. Replaces solution code with `raise NotImplementedError`

- General:
  1. Builds the conda environment localed in `src/environment` and executes the Jupyter Notebook to see that no errors occur in the Jupyter Notebook.

### How to access build results?

All these automations happen using a self-hosted Linux machine and GitHub Actions. On each commit that is pushed to GitHub, a little yellow dot will appear on the side of your commit, which indicates that the automated build is in progress. Clicking on it will reveal the result of the automated build. In this case, all the builds have passed:

<!-- Image removed for anonymity -->
<!-- ![Alt text](readme-diagrams/actions.png) -->

Click on *Details* and then click on *Summary* in the left corner.

<!-- Image removed for anonymity -->
<!-- ![Alt text](readme-diagrams/artifacts.png) -->

In the bottom, you will see all the created artifacts. **The most important artifact is student_files**, which contains all the student code, Jupyter Notebook code (both without any solutions), and the expected outputs pdf.
