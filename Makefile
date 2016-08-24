
test:
	python -m pytest tests

lint:
	pylint --rcfile .pylintrc mlab_api/*/**.py

prepare:
	mkdir -p bigtable_configs
	cp -r ../mlab-vis-pipeline/dataflow/data/bigtable/*.json ./bigtable_configs
	cp ../mlab-keys/mlab-cred.json cred.json

deploy: prepare
	gcloud app deploy
