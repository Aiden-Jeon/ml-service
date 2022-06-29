from typing import Dict
from pathlib import Path
import json
import yaml


class InferenceInTemplate:
    def __init__(self) -> None:
        self.header = """from typing import List
from pydantic import BaseModel, Field


class InferenceIn(BaseModel):
"""
        self.contents = []

    def add(self, name: str, data_type: str) -> None:
        data_type = "float" if data_type == "double" else data_type
        self.contents += [f"    {name}: List[{data_type}]"]

    def dump(self):
        contents = [self.header] + self.contents.copy()
        contents = "\n".join(contents)
        return contents


class SchemaGenerator:
    def __init__(self, artifact_path: str) -> None:
        self.artifact_path = Path(artifact_path)
        self.domain_root_path = Path(__file__).parent

    def load_input_example(self) -> None:
        with open(self.artifact_path / "input_example.json", "r") as f:
            self.input_example = json.load(f)

    def load_ml_model(self) -> Dict[str, str]:
        with open(self.artifact_path / "MLmodel", "r") as f:
            ml_model = yaml.safe_load(f)
        return ml_model

    def make_pydantic(self, ml_model: Dict[str, str]) -> InferenceInTemplate:
        input_schemas = ml_model["signature"]["inputs"]
        input_schemas = yaml.full_load(input_schemas)

        template = InferenceInTemplate()
        for input_schema in input_schemas:
            name = input_schema["name"]
            data_type = input_schema["type"]
            template.add(name, data_type)
        return template

    def dump_engine_schema(self, template: InferenceInTemplate) -> None:
        with open(self.domain_root_path / "engine" / "schema.py", "w") as f:
            print(template.dump())
            f.write(template.dump())
            f.write("\n")

    def load_schema(self) -> None:
        ml_model = self.load_ml_model()
        template = self.make_pydantic(ml_model)
        self.dump_engine_schema(template)
