# MLAB VIS API

**Work in progress.**

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
../../mlab_keys/mlab-oti-5235f008a07c.json
```

So ensure that directory and file is present.

2 - copies of the bigtable config files. It looks for them in:

```
../pipeline/dataflow/data/bigtable/
```

So make sure they are present and up-to-date

3 - the `gcloud` command line tool.

Currently, `gcloud app deploy` is used to deploy.
Ensure you have this tool installed and configured properly.

The app will be deployed and accessible from:

[https://mlab-api-dot-mlab-oti.appspot.com/](https://mlab-api-dot-mlab-oti.appspot.com/)

Right now there is a `connection` API call so you can see that the bigtable connection was made succesfully.

[https://mlab-api-dot-mlab-oti.appspot.com/connection](https://mlab-api-dot-mlab-oti.appspot.com/connection)

Example Queries:

[https://mlab-api-dot-mlab-oti.appspot.com/locations/AF+EG+11+Garden%20City/time/month/clientisps/AS24863/metrics](https://mlab-api-dot-mlab-oti.appspot.com/locations/AF+EG+11+Garden%20City/time/month/clientisps/AS24863/metrics)

[https://mlab-api-dot-mlab-oti.appspot.com/locations/NA+US+NY+New%20York/time/month/metrics](https://mlab-api-dot-mlab-oti.appspot.com/locations/NA+US+NY+New%20York/time/month/metrics)



## Configuration

Configs live in `config.py`.

## Organization

### Flask Stuff

Most of the flask app is currently in:

```
main.py
```

### Bigtable

Bigtable connection is currently in:

```
app/data/data.py
```

### Config reading

A lot of the functionality of the bigtable side of things comes from
reading our bigtable config files.

This functionality is implemented in

```
app/data/table_config.py
```

## Test

Test requirements are stored in a separate `requirements-test.txt` file.

Install with:

```
pip install -r requirements-test.txt
```

Then run tests with:

```
make test
```
