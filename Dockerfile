FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# no need to copy this, will take it from the venv .toml & uv.lock
# RUN pip install pandas pyarrow

WORKDIR /code
# we select the path to the python from the v.environment --> no need to use uv run python 
ENV PATH="/code/.venv/bin:$PATH" 

# copy from the general environment into the docker image
COPY pyproject.toml .python-version uv.lock ./

# to install the dependencies that come from the environment
RUN uv sync --locked

COPY ingest_data.py .

ENTRYPOINT ["python", "ingest_data.py"]