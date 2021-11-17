setup:
	pip install -r requirements.txt

import_data:
	cd src && python3 -m import_data

import_data_keep_tables:
	cd src && python3 -m import_data --keep

import_data_drop_tables:
	cd src && python3 -m import_data --drop

lint:
	flake8 src

test:
	pytest -v

coverage:
	pytest --cov=src src/tests/ --cov-config=.coveragerc 

run:
	cd src && uvicorn main:app --reload  