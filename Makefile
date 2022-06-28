init:
	poetry install

run-mlflow:
	poetry run mlflow server --host 0.0.0.0 --backend-store-uri="$(PWD)/mlruns"

run-server:
	PYTHONPATH=src/deployment/ poetry run uvicorn main:app --reload
