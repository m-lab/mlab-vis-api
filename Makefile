setup:
	pip install -t lib -r requirements.txt
	pip install -t lib -r requirements-test.txt
	pip install -t lib -r git-hooks/requirements-python.txt

test:
	GOOGLE_APPLICATION_CREDENTIALS=cred.json python -m pytest tests

clean:
	find . -name *.pyc -delete

lint:
	pylint --rcfile git-hooks/pylintrc mlab_api/*/**.py

prepare: clean
	mkdir -p bigtable_configs
	cp -r ../mlab-vis-pipeline/dataflow/data/bigtable/*.json ./bigtable_configs

run:
	GOOGLE_APPLICATION_CREDENTIALS=cred.json python main.py

deploy: clean
	gcloud app deploy
