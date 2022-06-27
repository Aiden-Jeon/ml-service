from pathlib import Path
import json
import yaml
import cloudpickle


class PydanticTemplate:
    def __init__(self) -> None:
        self.header = """from pydantic import BaseModel


class ModelInputSchema(BaseModel):
"""
        self.contents = []

    def add(self, name: str, data_type: str) -> None:
        data_type = "float" if data_type == "double" else data_type
        self.contents += [f"    {name}: {data_type}"]

    def dump(self):
        contents = [self.header] + self.contents.copy()
        contents = "\n".join(contents)
        return contents


class ModelEngine:
    def __init__(self, artifact_path: str, model_name: str) -> None:
        self.artifact_path = Path(artifact_path) / model_name
        self.model = ...
        self.ml_model = ...
        self.input_example = ...

    def _load_model(self) -> None:
        with open(self.artifact_path / "model.pkl", "rb") as f:
            self.model = cloudpickle.load(f)

    def _load_input_example(self) -> None:
        with open(self.artifact_path / "input_example.json", "r") as f:
            self.input_example = json.load(f)

    def _load_ml_model(self) -> None:
        with open(self.artifact_path / "MLmodel", "r") as f:
            self.ml_model = yaml.safe_load(f)

    def _make_pydantic(self) -> None:
        input_schemas = self.ml_model["signature"]["inputs"]
        input_schemas = yaml.full_load(input_schemas)

        template = PydanticTemplate()
        for input_schema in input_schemas:
            name = input_schema["name"]
            data_type = input_schema["type"]
            template.add(name, data_type)

        with open("schema.py", "w") as f:
            print(template.dump())
            f.write(template.dump())
            f.write("\n")

    def load_schema(self) -> None:
        self._load_ml_model()
        self._make_pydantic()

    def load(self) -> None:
        self._load_model()
