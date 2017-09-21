# MLAB VIS API

## What

Python Flask server connected to Bigtable to serve up data needed for MLab
Visualization.
This is a Python 2.* application.
You can run this application locally with Docker.

## Install

### Clone

There are githooks and travis files setup in this repository. You can either
clone this repo with the `--recursive` flag to fetch them like so:
`git clone --recursive <...>` or you can run `git submodule update --init` after
a basic clone.

### Prepare Bigtable configuration files

The bigtable configuration files that are used in the `mlab-vis-pipeline`.
These file are used to create the bigtable tables AND determine the correct
query format within this application. For that purpose, we copy them from that
repo here. The make script assumes you have `mlab-vis-pipeline` checked out in
the same parent folder.

Run `make prepare` to copy over necessary files.

### Bring over credential file

In order to access the bigtable tables in the desired environment (staging,
production or sandbox), you need to use a service account that you can
authenticate with. You should recieve a credential json file from an m-lab team
member or setup your own.
Create a folder **outside** of the root of this repository where you will store
these files.

### Build docker image

`docker build -t data-api .`

### Run Docker Image

You can run a local server like so:

```
docker run -p 8080:8080 \
-e KEY_FILE=/keys/<keyname>.json \
-v <local folder containing your secret keys>:/keys \
-e API_MODE=production|staging|sandbox data-api
```

Note that you need to create a mapping to the folder containing your keys.
For example, if my local keys live in `~/dev/mlab-keys` and the file name for the
production environment is `production-key.json` this command would look like:

```
docker run -p 8080:8080 \
-e KEY_FILE=/keys/production-key.json \
-v /Users/iros/dev/keys:/keys \
-e API_MODE=production|staging|sandbox data-api
```

The environment you choose to run in needs to have the appropriate
service key available as a json file.

Once the docker image is running, you should be able to access it at
[http://localhost:8080](http://localhost:8080).

The `API_MODE` flag will also choose one of the `environments/*` files to run.
Check those vars to ensure they match your expected settings, but they should
be generic enough to match all environments.

## Deploy

We use a flexible [App Engine](https://console.cloud.google.com/appengine)
deployment.

To deploy to app engine, run this simple command:
`KEY_FILE=<absolute path to your cred file> ./deploy.sh production|staging|sandbox`

Currently, `gcloud app deploy` is used to deploy internally.
Ensure you have this tool installed and configured properly.

The app will be deployed and accessible from the service URL which depends on
the environment. In production this URL is:

[https://data-api.measurementlab.net/](https://data-api.measurementlab.net/)

The API is documented at this url as well.

## Testing

You can build a test docker container by calling:

`docker build -f TestDockerFile -t data-api-test .`

Note that you need to have built your `data-api` container at least once for
this to work, since it uses it as a baseline.

To run the container you can call:

```
docker run \
-e KEY_FILE=/keys/<keyname>.json \
-v <local folder containing your secret keys>:/keys \
-e API_MODE=production|staging|sandbox data-api-test
```

Note this is a similar call except we don't pass in a port, since we aren't
running a web server for testing purposes. You still need to pass in a key
for the environment you're testing against, but the default tests have been
written against production data (we should really refactor them.)

Note, you should also lint your code before you consider PRing it.
You can do so by calling `./lint.sh`.

## Code

This code depends heavily on the [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) package.

It uses the [google api python client](http://google.github.io/google-api-python-client/docs/epy/index.html)
for communicating with BigTable.

## Troubleshooting

If you are getting errors about your inability to authenticate with the Google
Cloud Services such as:

```
ERROR: (gcloud.auth.activate-service-account) Invalid value for [ACCOUNT]: The
given account name does not match the account name in the key file.  This
argument can be omitted when using .json keys.
```

Try to authenticate the service account required. You can do this step after
calling `make prepare`.

`gcloud auth activate-service-account <service acccount email address> --key-file <cred file>.json`