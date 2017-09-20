# MLAB VIS API

## What

Python Flask server connected to Bigtable to serve up data needed for MLab Visualization.
This is a Python 2.* application.
You can run this application locally with Docker.

## Install

### Clone

There are githooks and travis files setup in this repository. You can either clone this repo with the `--recursive` flag
to fetch them like so: `git clone --recursive <...>` or you can
run `git submodule update --init` after a basic clone.

### Prepare Bigtable configuration files

The bigtable configuration files that are used in the `mlab-vis-pipeline`. These file are used to create the bigtable tables AND determine the correct query format within this application. For that purpose, we copy them from that repo here. The make script assumes you have `mlab-vis-pipeline` checked out in the same parent folder.

Run `make prepare` to copy over necessary files.

### Bring over credential file

In order to access the bigtable tables in the desired environment (staging, production or sandbox), you need to use a service account that you can authenticate with. You should recieve a credential json file from an m-lab team member or setup your own.
Copy that file and name it `cred.json` in the root of the application.

### Build docker image

`docker build -t data-api .`

Everytime you change your cred.json you'll need to rebuild the image.

### Run Docker Image

`docker run -p 8080:8080 -e API_MODE=production|staging|sandbox data-api`

Note that the environment you choose to run in needs to have the appropriate service key available as a `cred.json` file. Make sure you copy that over in advance.
Once the docker image is running, you should be able to access it at [http://localhost:8080](http://localhost:8080).

The `API_MODE` flag will also choose one of the `environments/*` files to run. Check those vars to ensure they match your expected settings.

## Deploy

We can deploy to flexibe [App Engine](https://console.cloud.google.com/appengine)!

To deploy to app engine, run this simple command: `KEY_FILE=<pathToYourCredFile> ./deploy.sh production|staging|sandbox`

Currently, `gcloud app deploy` is used to deploy internally.
Ensure you have this tool installed and configured properly.

The app will be deployed and accessible from the service URL which depends on the environment.
In production this URL is:

[https://data-api.measurementlab.net/](https://data-api.measurementlab.net/)

The API is documented at this url as well.

## Testing

Call `make setup` to install dependencies.

Since this is a python application, requirements need to be installed. There are 3 sets of requirements: Main application, testing environment and the git-hooks.
Make sure you've initialized your local submodule.

_Suggestion:_ Have a conda environment active before installing packages. If you do not have a conda environment setup, you may need to sudo install some of the requirements.

You can call `KEY_FILE=<path to your cred.json file> ./test.sh production|staging|sandbox`.

Note, you should also lint your code before you consider PRing it. You can do so by calling `./lint.sh`.

_Note_: The tests were written to data that is in production. We should probably refactor them to be slightly more generic.

## Code

This code depends heavily on the [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) package.

It uses the [google api python client](http://google.github.io/google-api-python-client/docs/epy/index.html) for communicating with BigTable.

## Troubleshooting

If you are getting errors about your inability to authenticate with the Google Cloud Services such as:

```
ERROR: (gcloud.auth.activate-service-account) Invalid value for [ACCOUNT]: The given account name does not match the account name in the key file.  This argument can be omitted when using .json keys.
```

Try to authenticate the service account required. You can do this step after calling `make prepare`

`gcloud auth activate-service-account <service acccount email address> --key-file <cred file>.json`