
test:
	python -m pytest tests

clean:
	find . -name *.pyc -delete

lint:
	pylint --rcfile .pylintrc mlab_api/*/**.py

prepare: clean
	mkdir -p bigtable_configs
	cp -r ../mlab-vis-pipeline/dataflow/data/bigtable/*.json ./bigtable_configs
	cp ../mlab-keys/mlab-cred.json cred.json

deploy: clean
	gcloud app deploy
