import os

import mlflow
import pandas as pd
from mlflow.models.signature import infer_signature
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

MODEL_REGISTRY_URL = os.getenv("MODEL_REGISTRY_URL", "http://localhost:5000")
mlflow.set_tracking_uri(MODEL_REGISTRY_URL)


def generate_sample() -> pd.DataFrame:
    x, y = make_regression(n_features=4, n_informative=3)

    x = pd.DataFrame(x).add_prefix("feature_")
    y = pd.Series(y, name="target")
    df = pd.concat([x, y], axis="columns")
    return df


def train_model(df: pd.DataFrame) -> LinearRegression:
    x, y = df.drop("target", axis="columns"), df["target"]
    train_x, valid_x, train_y, valid_y = train_test_split(x, y, test_size=0.2)
    regressor = LinearRegression()
    regressor.fit(train_x, train_y)

    train_pred = regressor.predict(train_x)
    train_mse = ((train_y - train_pred) ** 2).mean()
    mlflow.log_metric("train_mse", train_mse)

    valid_pred = regressor.predict(valid_x)
    valid_mse = ((valid_y - valid_pred) ** 2).mean()
    mlflow.log_metric("valid_mse", valid_mse)

    mlflow.sklearn.log_model(
        regressor,
        "model",
        signature=infer_signature(train_x.sample(1), train_pred[:1]),
        pip_requirements=["scikit-learn==1.1.1"],
    )
    return regressor


df = generate_sample()
train_model(df)
