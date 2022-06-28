from pathlib import Path
import json
import yaml


class InputPydanticTemplate:
    def __init__(self) -> None:
        self.header = """from pydantic import BaseModel, Field


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


class OutputPydanticTemplate:
    def __init__(self) -> None:
        self.header = """from pydantic import BaseModel, Field


class ModelOutputSchema(BaseModel):
"""
        self.contents = []

    def add(self, name: str, data_type: str) -> None:
        data_type = "float" if data_type == "double" else data_type
        self.contents += [f"    {name}: {data_type}"]

    def dump(self):
        contents = [self.header] + self.contents.copy()
        contents = "\n".join(contents)
        return contents


class SchemaGeneartor:
    def __init__(self, artifact_path: str, model_name: str) -> None:
        self.artifact_path = Path(artifact_path) / model_name
        self.ml_model = ...
        self.input_example = ...

    def _load_input_example(self) -> None:
        with open(self.artifact_path / "input_example.json", "r") as f:
            self.input_example = json.load(f)

    def _load_ml_model(self) -> None:
        with open(self.artifact_path / "MLmodel", "r") as f:
            self.ml_model = yaml.safe_load(f)

    def _make_pydantic(self, path: str) -> None:
        input_schemas = self.ml_model["signature"]["inputs"]
        input_schemas = yaml.full_load(input_schemas)

        template = InputPydanticTemplate()
        for input_schema in input_schemas:
            name = input_schema["name"]
            data_type = input_schema["type"]
            template.add(name, data_type)

        with open(Path(path) / "schema.py", "w") as f:
            print(template.dump())
            f.write(template.dump())
            f.write("\n")

    def load_schema(self, path) -> None:
        self._load_ml_model()
        self._make_pydantic(path)


generator = SchemaGeneartor("./", "model")
generator.load_schema("./engine")
