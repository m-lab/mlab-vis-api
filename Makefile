
test:
	python -m pytest tests

lint:
	pylint --rcfile .pylint textkit/*/**.py

prepare:
	mkdir -p bigtable_configs
	cp -r ../mlab-research/pipeline/dataflow/data/bigtable/ ./bigtable_configs
	cp ../mlab-keys/mlab-cred.json cred.json

deploy: prepare
	gcloud app deploy
