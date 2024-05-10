# Use the miniconda base image
FROM continuumio/miniconda3:latest

# Arguments to pass UID and GID
ARG USER_ID
ARG GROUP_ID

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    wkhtmltopdf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Files
COPY src/environment/ml_hw2_env_linux.yml /app/
COPY pyproject.toml poetry.lock /app/

# Create the Conda environment
RUN conda env create -f ml_hw2_env_linux.yml && \
    conda clean -afy && \
    rm ml_hw2_env_linux.yml

# Activate the Conda environment and install Poetry
RUN echo "source activate ml_hw2" > ~/.bashrc
ENV PATH /opt/conda/envs/ml_hw2/bin:$PATH
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir poetry && \
    python3 -m poetry config virtualenvs.create false && \
    python3 -m poetry install --no-cache --no-root

# Set environment variables
ENV LANG=en_US.UTF-8 \
    LC_CTYPE=UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    PYTHONUTF8=1 \
    PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring

# Create a non-root user and group with the provided UID and GID, only if they don't already exist
RUN if getent group ${GROUP_ID} ; then echo "Group ${GROUP_ID} already exists"; else groupadd -g ${GROUP_ID} appuser; fi && \
    if id -u ${USER_ID} ; then echo "User ${USER_ID} already exists"; else useradd -l -u ${USER_ID} -g ${GROUP_ID} -m appuser; fi && \
    install -d -m 0755 -o ${USER_ID} -g ${GROUP_ID} /home/appuser

# Change ownership of the /app directory
RUN chown appuser /app

# Copy the entry point script and set permissions
COPY src/utils/build-conda/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown appuser /entrypoint.sh

# Set the user to appuser
USER appuser

# Set the entry point
ENTRYPOINT ["/entrypoint.sh"]