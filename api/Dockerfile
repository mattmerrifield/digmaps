# onbuild docker image automatically runs pip install on requirements.txt
FROM python:3

# Additional utilities
RUN apt-get update && apt-get install -y \
    postgresql-client \
    binutils \
    libproj-dev \
    gdal-bin \
    postgresql-server-dev-all

# Gotta stuff the code somewhere and make it visible to python
WORKDIR /code
COPY . /code
ENV PYTHONPATH $PYTHONPATH:/code

# Pip last, since these things change so frequently, we'll rebuild them almost
# every time
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "./digmaps/manage.py", "runserver", "0.0.0.0:8080"]

