# MLAB VIS API

## What

Python Flask server connected to Bigtable to serve up data needed for MLab Visualization.

## Install

### Clone

There are githooks setup in this repository. You can either clone this repo with the `--recursive` flag 
to fetch them like so: `git clone --recursive <...>` or you can 
run `git submodule update --init` after a basic clone.

### Setup

Call `make setup`
Since this is a python application, requirements need to be installed. There are 3 sets of requirements: Main application, testing environment and the git-hooks. 
Make sure you've initialized your local submodule. 

_Suggestion:_ Have a conda environment active before installing packages. If you do not have a conda environment setup, you may need to sudo install some of the requirements. This is a Python 2.* application.

### Point to credential files

In order to access the bigtable tables in production, you need to use a service account that you can authenticate with. You should recieve them from an m-lab team member or setup your own. You will need to update the variables set in the `environments/*.sh` files to reflect the paths to those files before you run the server! 

### Prepare Bigtable configuration files

The bigtable configuration files that are used in the `mlab-vis-pipeline`. These file are used to create the bigtable tables AND determine the correct query format within this application. For that purpose, we copy them from that repo here. The make script assumes you have `mlab-vis-pipeline` checked out in the same parent folder.

Run `make prepare` to copy over necessary files. 

## Run

Start flask server by calling `./run.sh production|staging|sandbox`

## Deploy

We can deploy to flexibe [App Engine](https://console.cloud.google.com/appengine)!

To deploy to app engine, run this simple command: `./deploy.sh production|staging|sandbox`

Currently, `gcloud app deploy` is used to deploy internally.
Ensure you have this tool installed and configured properly.

The app will be deployed and accessible from:

[https://data-api.measurementlab.net/](https://data-api.measurementlab.net/)

The API is documented at this url as well.

## Testing

Test requirements are stored in a separate `requirements-test.txt` file. They should be installed when you called `make setup`. If they did not, you can run it manually as well: `pip install -r requirements-test.txt`

Then run tests with: `make test`

## code

This code depends heavily on the [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) package.

It uses the [google api python client](http://google.github.io/google-api-python-client/docs/epy/index.html) for communicating with BigTable.

## Troubleshooting

If you are getting errors about your inability to authenticate with the Google Cloud Services such as:

```
ERROR: (gcloud.auth.activate-service-account) Invalid value for [ACCOUNT]: The given account name does not match the account name in the key file.  This argument can be omitted when using .json keys.
```

Try to authenticate the service account required. You can do this step after calling `make prepare`

`gcloud auth activate-service-account <service acccount email address> --key-file <cred file>.json`