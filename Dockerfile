FROM gcr.io/google-appengine/python
MAINTAINER Irene Ros <imirene@gmail.com>

# Pass in appropriate key
ARG KEY_FILE=cred.json

RUN apt-get update && apt-get install -y rsync tar python-dev python-pip

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
RUN virtualenv /env

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Add the application source code.
ADD . /mlab-vis-api
# Set the working directory to /mlab-vis-api
WORKDIR /mlab-vis-api

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
ADD requirements.txt /mlab-vis-api/requirements.txt
RUN pip install -r /mlab-vis-api/requirements.txt

# Port
EXPOSE 8080

STOPSIGNAL SIGTERM

# Run based on the environment. API_MODE should be production, staging or sandbox.
CMD ./run.sh $API_MODE