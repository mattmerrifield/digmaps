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
ENV PYTHONPATH $PYTHONPATH:/code
EXPOSE 80

# pip install only when the reqirements change
COPY frozen_requirements.txt .
RUN pip install --no-cache-dir -r frozen_requirements.txt

# Add the whole code directory later so we don't trigger a rebuild
# every time *anything* in the repo changes; only for some stuff
COPY . /code

EXPOSE 8000
CMD ["python", "manage.py", "runserver_plus","--nopin", "0.0.0.0:8000"]

