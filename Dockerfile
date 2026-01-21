FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# no need to copy this, will take it from the venv .toml 
# RUN pip install pandas pyarrow

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"

# copy from the general environment into the docker image
COPY pyproject.toml .python-version uv.lock ./

# to install the dependencies that come from the environment
RUN uv sync --locked

COPY pipeline/pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]