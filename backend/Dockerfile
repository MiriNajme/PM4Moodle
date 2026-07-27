# PM4Moodle backend (Flask + pm4py) for the Docker demo.
FROM python:3.12-slim

# graphviz is required by pm4py to render the OC-DFG visualization (PNG).
RUN apt-get update \
    && apt-get install -y --no-install-recommends graphviz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first so this layer is cached across code changes.
# requirements.txt pins everything to prebuilt wheels (see the --only-binary
# note in that file), so no compiler is needed in the image.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Application code.
COPY . .

ENV FLASK_APP=app.py \
    PYTHONUNBUFFERED=1

EXPOSE 5000

ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]
