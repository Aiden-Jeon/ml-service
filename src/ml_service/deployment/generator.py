import json
from pathlib import Path
from typing import Dict

import yaml

from ml_service.deployment.templates import DataInTemplate, InferenceInTemplate


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

    def make_orm(self, ml_model: Dict[str, str]) -> DataInTemplate:
        input_schemas = ml_model["signature"]["inputs"]
        input_schemas = yaml.full_load(input_schemas)

        template = DataInTemplate()
        for input_schema in input_schemas:
            name = input_schema["name"]
            data_type = input_schema["type"]
            template.add(name, data_type)
        return template

    def write_pydantic(
        self,
        template: InferenceInTemplate,
        domain: str,
        filename: str,
        content: str = "list",
    ) -> None:
        with open(self.domain_root_path / domain / filename, "w") as f:
            f.write(template.dump(content=content))
            f.write("\n")

    def write_orm(self, template: DataInTemplate, domain: str, filename: str) -> None:
        with open(self.domain_root_path / domain / filename, "w") as f:
            f.write(template.dump())
            f.write("\n")

    def load_schema(self) -> None:
        ml_model = self.load_ml_model()
        pydantic_template = self.make_pydantic(ml_model)
        self.write_pydantic(pydantic_template, "engine", "schema.py", "list")
        self.write_pydantic(pydantic_template, "buffer", "schema.py", "single")

        orm_template = self.make_orm(ml_model)
        self.write_orm(orm_template, "buffer", "model.py")
