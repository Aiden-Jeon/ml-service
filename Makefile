init:
	poetry install

init-db:
	initdb -D mnt/psql/data

init-user:
	psql -d postgres -c "CREATE USER postgres WITH PASSWORD 'password';"
	psql -d postgres -c "\du"

run-postgres:
	postgres -D mnt/psql/data

run-mlflow:
	poetry run mlflow server --host 0.0.0.0 --backend-store-uri="$(PWD)/mlruns"

clean-postgres:
	rm -rf mnt/psql

clean-mlflow:
	rm -rf mlruns/

run-server:
	PYTHONPATH=src/deployment/ poetry run uvicorn main:app --reload

format:
	poetry run black .
	poetry run isort . --skip-gitignore --profile black

lint:
	PYTHONPATH=src/ poetry run pytest src/ --pylint --flake8 --ignore-glob=src/**/schema.py --ignore-glob=src/**/model.py
