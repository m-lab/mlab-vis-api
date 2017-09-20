FROM gcr.io/google-appengine/python
LABEL maintainer="Irene Ros <imirene@gmail.com>"

LABEL python_version=python
RUN virtualenv --no-download /env -p python

# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate
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

CMD ./run.sh $API_MODE
