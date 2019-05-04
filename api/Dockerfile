# onbuild docker image automatically runs pip install on requirements.txt
FROM python:3.6

# Additional utilities
RUN apt-get update && apt-get install -y \
    postgresql-client \
    binutils \
    libproj-dev \
    gdal-bin \
    postgresql-server-dev-all \
    nmap

# Gotta stuff the code somewhere and make it visible to python
WORKDIR /code
COPY . /code
ENV PYTHONPATH $PYTHONPATH:/code
EXPOSE 80

# Pip last, since these things change so frequently, we'll rebuild them almost
# every time
RUN pip install --no-cache-dir -r frozen_requirements.txt
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:80"]

