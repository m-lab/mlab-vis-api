setup:
	pip install -t lib -r requirements.txt
	pip install -t lib -r requirements-test.txt
	pip install -t lib -r git-hooks/requirements-python.txt

clean:
	find . -name *.pyc -delete

prepare: clean
	mkdir -p bigtable_configs
	cp -r ../mlab-vis-pipeline/dataflow/data/bigtable/*.json ./bigtable_configs
