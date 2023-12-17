FROM python:3.11.3-slim-buster

# Install gcc.
RUN apt-get update \
&& apt-get install libpq-dev gcc libgl1-mesa-glx libglib2.0-0 -y \
&& apt-get clean

# Set working directory.
WORKDIR /src
ADD . /src

# Installing dependencies.
RUN pip install poetry --upgrade
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root

ENTRYPOINT ["gunicorn", "-c", "python:gunicorn_config", "-k", "uvicorn.workers.UvicornWorker", "app.api:create_app"]
