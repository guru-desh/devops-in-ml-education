# Use the Gradescope autograder base image
FROM gradescope/autograder-base:ubuntu-22.04

# Define an argument for the ZIP file URL
ARG ZIP_FILE

# Create a directory for the autograder source
RUN mkdir -p /autograder/source

# Add the autograder ZIP file using the argument
ADD ${ZIP_FILE} /tmp/autograder.zip

# Unzip the autograder files
RUN unzip -n -d /autograder/source /tmp/autograder.zip

# Copy the run_autograder script
RUN cp /autograder/source/run_autograder /autograder/run_autograder

# Convert line endings and make the script executable
RUN apt-get update && apt-get install -y dos2unix
RUN dos2unix /autograder/run_autograder /autograder/source/setup.sh
RUN chmod +x /autograder/run_autograder

# Execute the setup script
RUN bash /autograder/source/setup.sh
