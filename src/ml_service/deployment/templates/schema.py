class InferenceInTemplate:
    def __init__(self) -> None:
        self.header = """from typing import List
from pydantic import BaseModel


class InferenceIn(BaseModel):
"""
        self.list_contents = []
        self.single_contents = []

    def add(self, name: str, data_type: str) -> None:
        data_type = "float" if data_type == "double" else data_type
        self.list_contents += [f"    {name}: List[{data_type}]"]
        self.single_contents += [f"    {name}: {data_type}"]

    def dump(self, content: str) -> str:
        if content == "list":
            contents = self.list_contents.copy()
        elif content == "single":
            contents = self.single_contents.copy()
        else:
            raise ValueError("Not valid content %s, supported content is  'list' and 'single'" % data_type)
        contents = [self.header] + contents
        contents = "\n".join(contents)
        return contents
