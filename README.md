# MLAB VIS API

## What

Python Flask server connected to Bigtable to serve up data needed for MLab Visualization.

## Install

Required packages can be installed via:

```
pip install -r requirements.txt
```

_Suggestion:_ Have a conda environment active before installing packages.

## Run

Start Flask server via

```
python main.py
```

## Deploy

We can deploy to flexibe [App Engine](https://console.cloud.google.com/appengine)!

To deploy to app engine, run this simple command:

```
make deploy
```

Well, its not really that simple. For this to work, it requires a few things:

1 - access to your Google Service Account JSON file. It currently looks for it in:

```
../mlab-keys/mlab-cred.json
```

So ensure that directory and file is present.

2 - copies of the bigtable config files. It looks for them in:

```
../mlab-vis-pipeline/dataflow/data/bigtable/
```

You can use `make prepare` to copy the appropriate config files from the pipeline to the api.

So make sure they are present and up-to-date

3 - the `gcloud` command line tool.

Currently, `gcloud app deploy` is used to deploy.
Ensure you have this tool installed and configured properly.

The app will be deployed and accessible from:

[http://data-api.measurementlab.net/](http://data-api.measurementlab.net/)

The API is documented at this url as well.

## Testing

Test requirements are stored in a separate `requirements-test.txt` file.

(So that the deploy code does not need to download these additional requirements).

Install with:

```
pip install -r requirements-test.txt
```

Then run tests with:

```
make test
```

## code

This code depends heavily on the [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) package.

It uses the [google api python client](http://google.github.io/google-api-python-client/docs/epy/index.html) for communicating with BigTable.
