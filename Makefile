setup: requirements.txt
    pip install -r requirements.txt

import_data:
	python3 -m src.import_data

lint:
	flake8 src

test:
	pytest -v

coverage: .coveragerc 
	pytest --cov=src src/tests/ --cov-config=.coveragerc 

run:
	cd src && uvicorn main:app --reload  