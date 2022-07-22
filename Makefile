init:
	poetry install

init-db:
	initdb --username=user --pwprompt -D mnt/psql/data

run-postgres:
	postgres -D mnt/psql/data

run-mlflow:
	poetry run mlflow server --host 0.0.0.0 --backend-store-uri="$(PWD)/mlruns"

run-server:
	PYTHONPATH=src/deployment/ poetry run uvicorn main:app --reload

format:
	poetry run black .
	poetry run isort . --skip-gitignore --profile black

lint:
	PYTHONPATH=src/ poetry run pytest src/ --pylint --flake8 --ignore-glob=src/**/schema.py --ignore-glob=src/**/model.py
