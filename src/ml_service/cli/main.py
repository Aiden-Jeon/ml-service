import os
from pathlib import Path

import typer

from ml_service.cli.download import download_artifact, get_artifact_uri
from ml_service.deployment.generator import SchemaGenerator

app = typer.Typer(help="ml-service command line tool")
SRC_PATH = Path(__file__).parents[1]
DEPLOYMENT_PATH = SRC_PATH / "deployment"


@app.command()
def sync(
    run_id: str = typer.Option(..., help="run_id in mlflow"),
    tracking_uri: str = typer.Option(
        "http://localhost:5000", help="tracking uri to get mlflow artifacts",
    ),
    dest_path: str = typer.Option("mnt/artifacts", help="path to download artifacts"),
) -> None:
    artifact_path = get_artifact_uri(tracking_uri=tracking_uri, run_id=run_id)
    download_artifact(artifact_path=artifact_path, dest_path=dest_path)


@app.command()
def server(
    artifact_path: str = typer.Option(
        "mnt/artifacts", help="path of artifact to run server",
    ),
    model_name: str = typer.Option(..., help="name of model to deploy"),
) -> None:
    model_artifact_path = Path(artifact_path) / model_name
    generator = SchemaGenerator(model_artifact_path)
    generator.load_schema()
    cmd = f"PYTHONPATH={DEPLOYMENT_PATH} MODEL_ARTIFACT_PATH={model_artifact_path} poetry run uvicorn main:app --reload"
    os.system(cmd)
