import os
from mlflow.tracking import MlflowClient


def get_artifact_uri(tracking_uri: str, run_id: str) -> str:
    client = MlflowClient(tracking_uri=tracking_uri)
    run = client.get_run(run_id)
    artifact_uri = run.info.artifact_uri
    return artifact_uri


def download_artifact(artifact_path: str, dest_path: str) -> None:
    cmd = "rclone sync %s %s" % (artifact_path, dest_path)
    os.system(cmd)
