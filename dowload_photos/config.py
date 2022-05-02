import yaml
from pydantic import BaseModel


class Database(BaseModel):
    username: str
    password: str
    host: str
    port: int
    db_name: str


def load_yaml(file) -> dict:
    with open(file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


db = Database(**load_yaml("../config.yml"))
