def _convert_data_type(data_type: str) -> str:
    converter = {
        "double": "Float",
        "int": "Integer",
        "str": "String",
    }
    result = converter.get(data_type, False)
    if not result:
        raise ValueError("Cannot convert given data_type %s" % data_type)
    return result


class DataInTemplate:
    def __init__(self) -> None:
        self.header = """from datetime import datetime


from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from ml_service.deployment.store import Base


class DataIn(Base):
    __tablename__ = "input"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

"""
        self.contents = []

    def add(self, name: str, data_type: str) -> None:
        data_type = _convert_data_type(data_type)
        self.contents += [f"    {name} = Column({data_type})"]

    def dump(self) -> str:
        contents = [self.header] + self.contents
        contents = "\n".join(contents)
        return contents


class DataOutTemplate:
    def __init__(self) -> None:
        self.header = """from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text



class DataOut:
    __tablename__ = "output"
    timestamp = Column(DateTime, default=datetime.utcnow)

"""

        self.contents = []

    def add(self, name: str, data_type: str) -> None:
        data_type = _convert_data_type(data_type)
        self.contents += [f"    {name}: Column({data_type})"]

    def dump(self) -> str:
        contents = [self.header] + self.contents
        contents = "\n".join(contents)
        return contents
